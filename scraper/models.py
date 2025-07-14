from pydantic import BaseModel

class OABRequest(BaseModel):
    name: str
    uf: str

class OABResponse(BaseModel):
    oab: str
    nome: str
    uf: str
    categoria: str
    data_inscricao: str
    situacao: str