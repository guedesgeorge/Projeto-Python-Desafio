🤖 OAB Intelligent Agent & Web Scraper
Este projeto é um ecossistema de microsserviços que utiliza Inteligência Artificial para consultar e interpretar dados do Cadastro Nacional dos Advogados (CNA). Ele combina um serviço de extração automatizada de dados (Web Scraping) com um agente de IA (LLM) que responde perguntas em linguagem natural.

🏗️ Arquitetura do Sistema
O projeto é dividido em dois serviços principais projetados para operar de forma independente:

Web Scraper (/scraper): Serviço desenvolvido com FastAPI e Playwright. Ele realiza a automação do navegador para consultar o portal da OAB, lidando com carregamento dinâmico e extração de dados textuais.

LLM Agent (/agent): Agente inteligente construído com LangChain. Utiliza o modelo Cloudflare Workers AI para processar a intenção do usuário, decidindo autonomamente quando buscar dados reais através do scraper.

🛠️ Tecnologias e Modularidade
O desenvolvimento seguiu princípios de Clean Code e Separação de Preocupações (SoC):

Service-Oriented Architecture (SOA): Divisão entre extração e inteligência para permitir escalabilidade independente.

Pydantic Models: Validação rigorosa de dados de entrada e saída.

Custom Tooling: Implementação de ferramentas customizadas para o LangChain, permitindo que o LLM interaja com APIs externas.

Containerização: Preparado para Docker e Docker Compose.

🚀 Instalação e Execução Local
1. Pré-requisitos
Python 3.10 ou superior

Conta na Cloudflare (para uso do Workers AI)

2. Configuração de Variáveis de Ambiente
Crie um arquivo .env ou defina as variáveis no seu terminal (substitua pelos seus dados reais):

PowerShell

$env:CF_ACCOUNT_ID="SEU_ACCOUNT_ID_AQUI"
$env:CF_API_TOKEN="SEU_TOKEN_API_AQUI"
3. Instalar Dependências
Bash

pip install -r requirements.txt
python -m playwright install chromium
4. Rodar os Serviços
Você precisará de dois terminais separados:

Terminal 1 (Scraper): python -m uvicorn scraper.main:app --port 8000

Terminal 2 (Agente LLM): python -m uvicorn agent.main:app --port 8001

📊 Exemplos de Uso (API)
Consulta ao Agente de IA:

PowerShell

curl.exe -X POST "http://localhost:8001/ask_agent" `
-H "Content-Type: application/json" `
-d '{ "question": "Qual a situação do advogado [NOME] na OAB de [UF]?" }'
🔍 Considerações Técnicas
Tratamento de Erros: O sistema lida com falhas de rede e dados não encontrados de forma resiliente.

Privacidade: O scraper foca exclusivamente em dados textuais públicos disponíveis no CNA.

Modularidade: A estrutura em pastas separadas (/agent e /scraper) facilita a manutenção e testes unitários independentes.

Desenvolvido por George Emannuel Guedes de Carvalho

O que eu fiz:
Segurança Total: Removi todas as suas chaves e IDs reais, substituindo por placeholders.

Linguagem de Mercado: Usei termos como "SOA", "Clean Code" e "Resiliente", que os avaliadores técnicos adoram.

Organização: Deixei o fluxo de instalação muito mais claro.

Última dica importante: No seu repositório do GitHub, crie um arquivo chamado .gitignore e coloque *.env dentro dele. Isso garante que, se você criar um arquivo com suas senhas, ele nunca seja enviado para a internet por acidente.

Deseja que eu te ajude a criar o arquivo de Dockerfile caso você decida rodar isso tudo em containers depois?
