# Visão Geral
O projeto é dividido em duas partes principais:

Web Scraper (scraper/): Um serviço FastAPI que consulta o site da OAB (https://cna.oab.org.br/) e extrai informações de advogados(as) com base no nome completo e UF.

Observação Importante: Durante o desenvolvimento, foi identificado que a extração de imagens de pessoas (fotos) do site da OAB não é viável com a abordagem atual de scraping, pois essas imagens não estão diretamente acessíveis ou são protegidas de alguma forma que impede a extração automatizada sem complexidade adicional. Portanto, o scraper foca apenas nos dados textuais solicitados.

LLM Agent (agent/): Um agente de IA construído com LangChain que utiliza um modelo de linguagem (Cloudflare Workers AI) e uma ferramenta customizada para interagir com o serviço do scraper e responder perguntas em linguagem natural sobre os dados da OAB.


# Estrutura do Projeto

├── scraper/

│   ├── __init__.py

│   ├── main.py

│   └── models.py

├── agent/

│   ├── __init__.py

│   ├── main.py

│   └── tools.py

├── requirements.txt

├── Dockerfile_scraper  # (Não usado na execução local, mas mantido para contexto Docker)

├── Dockerfile_agent    # (Não usado na execução local, mas mantido para contexto Docker)

├── docker-compose.yml  # (Não usado na execução local, mas mantido para contexto Docker)

└── README.md


# Instalação e Execução Local
Este guia detalha como rodar o projeto diretamente no seu ambiente local, sem a necessidade de Docker.

Pré-requisitos
Python 3.10 ou superior: Baixe e instale a versão mais recente do Python em python.org. Certifique-se de que pip está incluído na instalação.

Configuração das Variáveis de Ambiente
O agente LLM requer credenciais para acessar o Cloudflare Workers AI. Você precisará definir estas variáveis de ambiente na sua sessão de terminal antes de iniciar o serviço do agente.

$env:CF_ACCOUNT_ID="d0393f42f4b3c07bb4214c57372dbe6a"
$env:CF_API_TOKEN="ZTw7CxX6KLjeMAg20PSt2965arefWThtlKr99yA2"



Observação: Estas variáveis são válidas apenas para a sessão atual do terminal. Se você fechar o terminal, precisará defini-las novamente.

# Instalar Dependências
Abra seu terminal PowerShell na pasta raiz do projeto (C:\ProjetoOab) e instale todas as dependências Python:

pip install -r requirements.txt


# Em seguida, instale os navegadores necessários para o Playwright (usado pelo scraper):

python -m playwright install chromium

# Rodar os Serviços Localmente
Você precisará de dois terminais PowerShell separados para rodar os serviços do scraper e do agente simultaneamente. Navegue até a pasta raiz do projeto (C:\ProjetoOab) em ambos os terminais.


# Terminal 1: Rodar o Scraper

python -m uvicorn scraper.main:app --host 0.0.0.0 --port 8000 --reload

# Você deverá ver mensagens indicando que o Uvicorn está rodando na porta 8000.


# terminal 2: Rodar o Agente LLM
Neste terminal, primeiro defina as variáveis de ambiente (se ainda não o fez na sessão atual), e depois inicie o agente.


# Defina as variáveis de ambiente (apenas se ainda não estiverem definidas nesta sessão)
$env:CF_ACCOUNT_ID="d0393f42f4b3c07bb4214c57372dbe6a"
$env:CF_API_TOKEN="ZTw7CxX6KLjeMAg20PSt2965arefWThtlKr99yA2"

# Inicie o serviço do agente
python -m uvicorn agent.main:app --host 0.0.0.0 --port 8001 --reload



# Como Configurar o Cloudflare Workers AI
Para usar o Cloudflare Workers AI, você precisará de uma conta Cloudflare e um plano que inclua Workers AI.

# Crie uma conta Cloudflare (se ainda não tiver).

Obtenha seu CF_ACCOUNT_ID: Você pode encontrá-lo no painel do Cloudflare, na seção "Workers & Pages" ou nas configurações da sua conta.

Crie um Token de API:

Vá para My Profile > API Tokens > Create API Token.

Crie um token com as permissões apropriadas para Workers AI (por exemplo, "Workers AI: Invoke" ou uma permissão mais abrangente se necessário, mas com cautela).

Copie o token gerado.

Insira essas credenciais no arquivo .env (se você estivesse usando Docker) ou defina-as como variáveis de ambiente no terminal conforme descrito na seção "Configuração das Variáveis de Ambiente" para execução local.



# Exemplos de Uso
Com ambos os serviços (scraper na porta 8000 e agent na porta 8001) rodando, você pode testá-los usando curl em um terceiro terminal PowerShell.


# Consulta via API do Scraper (cURL)

curl.exe -X POST "http://localhost:8000/fetch_oab" `
     -H "Content-Type: application/json" `
     -d '{
           "name": "NOME DO ADVOGADO COMPLETO",
           "uf": "SP"
         }'


        Substitua "NOME DO ADVOGADO COMPLETO" e "SP" por dados reais de um advogado que você espera encontrar no site da OAB para teste.

Resposta esperada (exemplo):

{
  "oab": "123456",
  "nome": "NOME DO ADVOGADO COMPLETO",
  "uf": "SP",
  "categoria": "Advogado",
  "data_inscricao": "01/01/2000",
  "situacao": "Ativo"
}


Consulta via Agente LLM (cURL)
curl.exe -X POST "http://localhost:8001/ask_agent" `
     -H "Content-Type: application/json" `
     -d '{
           "question": "Qual é o número de inscrição e a situação atual do advogado Fulano de Tal na OAB de São Paulo?"
         }'


         {
  "response": "O advogado Fulano de Tal, com número de inscrição OAB 123456, tem a situação atual 'Ativo' na OAB de SP."
}


# Boas Práticas e Considerações
Tratamento de Erros: Ambos os serviços implementam tratamento de erros para lidar com falhas de rede, dados não encontrados e entradas inválidas.

Robustez do Scraper: O scraper utiliza Playwright para lidar com JavaScript e carregamento dinâmico. Seletores de CSS devem ser ajustados conforme a estrutura do site da OAB.

Prompt Engineering: O prompt do agente foi cuidadosamente elaborado para guiar o LLM a utilizar a ferramenta fetch_oab de forma eficaz.

Modularidade: O código é dividido em módulos lógicos (models.py, tools.py, main.py).
