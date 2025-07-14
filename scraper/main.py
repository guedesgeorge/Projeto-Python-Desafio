from fastapi import FastAPI, HTTPException
from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.prompts import PromptTemplate
from langchain_cloudflare.chat_models import ChatCloudflareWorkersAI
import os


app = FastAPI()

llm = ChatCloudflareWorkersAI(
    cloudflare_account_id=os.getenv("CF_ACCOUNT_ID"),
    cloudflare_api_token=os.getenv("CF_API_TOKEN"),
    model="@cf/tinyllama-1.1b-chat"
)

tools = [FetchOABTool()]

template = """
Responda às seguintes perguntas da melhor forma possível. Você tem acesso às seguintes ferramentas:

{tools}

Use o seguinte formato:

Pergunta: a pergunta de entrada que você deve responder
Pensamento: você deve sempre pensar no que fazer
Ação: a ação a ser tomada, deve ser uma das [{tool_names}]
Observação: o resultado da ação
... (este Pensamento/Ação/Observação pode se repetir várias vezes)
Pensamento: Eu sei a resposta final
Resposta Final: a resposta final para a pergunta original

Comece!

Pergunta: {input}
Pensamento:{agent_scratchpad}
"""

prompt = PromptTemplate.from_template(template)

agent = create_react_agent(llm, tools, prompt)

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)

@app.post("/ask_agent")
async def ask_agent(question: dict):
    user_question = question.get("question")
    if not user_question:
        raise HTTPException(status_code=400, detail="A pergunta não pode estar vazia.")
    
    try:
        response = agent_executor.invoke({"input": user_question})
        return {"response": response["output"]}
    except Exception as e:
        print(f"Erro no agente LLM: {e}")
        raise HTTPException(status_code=500, detail=f"Erro ao processar a pergunta: {e}")
