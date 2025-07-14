from fastapi import FastAPI, HTTPException
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import re
from typing import Optional

from .models import OABRequest, OABResponse

app = FastAPI() # <-- ESTA LINHA É FUNDAMENTAL E DEVE ESTAR AQUI, NA COLUNA 1!

def scrape_oab_data(name: str, uf: str) -> Optional[OABResponse]:
    url = "https://cna.oab.org.br/"
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)

        # Preencher os campos
        page.fill('input[name="nome"]', name)
        page.select_option('select[name="uf"]', uf)
        
        # Clicar no botão de busca
        page.click('button[type="submit"]')
        
        # Esperar pelos resultados. Pode ser necessário ajustar o seletor ou adicionar um timeout
        try:
            # AJUSTE ESTE SELETOR: Inspecione o HTML do site da OAB para o seletor correto da tabela/resultados
            page.wait_for_selector('div.panel-body table tbody tr', timeout=10000) 
        except Exception as e:
            print(f"Não foi possível encontrar os resultados ou o seletor: {e}")
            browser.close()
            return None 
        
        html_content = page.content()
        browser.close()

    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Encontrar a tabela de resultados. Adapte os seletores conforme a estrutura real do site da OAB
    table = soup.find('table', class_='table') # Pode ser outro seletor como id ou uma combinação de classes

    data = {}
    if table:
        rows = table.find_all('tr')
        if len(rows) > 1:
            # Exemplo de extração de dados. Adapte os índices [0], [1], etc.
            # e a lógica para pegar os dados corretos da tabela da OAB.
            try:
                data_cells = [td.get_text(strip=True) for td in rows[1].find_all('td')]

                data = {
                    "oab": data_cells[0] if len(data_cells) > 0 else "N/A",
                    "nome": data_cells[1] if len(data_cells) > 1 else "N/A",
                    "uf": data_cells[2] if len(data_cells) > 2 else "N/A",
                    "categoria": data_cells[3] if len(data_cells) > 3 else "N/A",
                    "data_inscricao": data_cells[4] if len(data_cells) > 4 else "N/A",
                    "situacao": data_cells[5] if len(data_cells) > 5 else "N/A",
                }
                return OABResponse(**data)
            except IndexError:
                print("Erro: Nem todas as colunas esperadas foram encontradas na tabela de resultados.")
                return None
            except Exception as e:
                print(f"Erro ao parsear os dados da tabela: {e}")
                return None
    
    print("Nenhuma tabela de resultados ou dados suficientes encontrados.")
    return None

@app.post("/fetch_oab", response_model=OABResponse)
async def fetch_oab(request: OABRequest):
    try:
        data = scrape_oab_data(request.name, request.uf)
        if data:
            return data
        raise HTTPException(status_code=404, detail="Advogado não encontrado ou dados indisponíveis.")
    except HTTPException: # Re-lança HTTPException já que ela foi levantada intencionalmente
        raise
    except Exception as e:
        print(f"Erro inesperado no endpoint /fetch_oab: {e}")
        raise HTTPException(status_code=500, detail=f"Erro interno no servidor: {e}")
