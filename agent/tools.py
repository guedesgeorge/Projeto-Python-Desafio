from langchain.tools import BaseTool
from pydantic import BaseModel, Field
import requests
from typing import Type

class FetchOABInput(BaseModel):
    name: str = Field(description="Nome completo do advogado.")
    uf: str = Field(description="UF da seccional do advogado (ex: SP, RJ).")

class FetchOABTool(BaseTool):
    name = "fetch_oab"
    description = """
    Útil para consultar dados de advogados no Cadastro Nacional dos Advogados da OAB.
    Requer o nome completo do advogado e a UF da seccional.
    Retorna o número da inscrição (OAB), nome completo, UF, categoria, data de inscrição e situação atual.
    """
    args_schema: Type[BaseModel] = FetchOABInput

    def _run(self, name: str, uf: str) -> str:
        # URL do seu serviço scraper (assumindo que rodará no mesmo docker-compose)
        scraper_url = "http://scraper:8000/fetch_oab" 
        try:
            response = requests.post(scraper_url, json={"name": name, "uf": uf})
            response.raise_for_status() # Lança um erro para status de erro HTTP
            data = response.json()
            return str(data) # Retorna os dados como string para o LLM
        except requests.exceptions.RequestException as e:
            return f"Erro ao consultar a OAB: {e}. Verifique se o nome e a UF estão corretos."

    async def _arun(self, name: str, uf: str) -> str:
        # Implementação assíncrona se necessário, mas para este caso _run é suficiente
        raise NotImplementedError("fetch_oab does not support async")