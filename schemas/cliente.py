from pydantic import BaseModel
from typing import Optional, List
from model.cliente import Cliente


class ClienteSchema(BaseModel):
    """
    Define como um novo cliente inserido deverá ser apresentado
    """
    nome: str = "Nome do Cliente"
    telefone: str = "00122334455"
    email: str = "meuemail@email.com"
    cpf: str = "00011122233"


class ClienteBuscaSchema(BaseModel):
    """
    Define como deve ser a estrutura que representa a busca. Que será
    feita apenas com base no CPF do cliente.
    """
    cpf: str = "CPF do cliente"


class ListagemClientesSchema(BaseModel):
    """
    Define como uma listagem de clientes será retornada.
    """
    cliente:List[ClienteSchema]


def apresenta_clientes(clientes: List[Cliente]):
    """
    Retorna uma apresentação do cliente seguindo o schema definido em
    ClienteViewSchema
    """
    result = []
    for cliente in clientes:
        result.append({
            "id": cliente.id,
            "nome": cliente.nome,
            "telefone": cliente.telefone,
            "email": cliente.email,
            "cpf": cliente.cpf
        })
    
    return {"clientes": result}


class ClienteViewSchema(BaseModel):
    """
    Define como um cliente será retornado.
    """
    id: int = 999
    nome: str = "Nome do Cliente"
    telefone: str = "00122334455"
    email: str = "emailcliente@email.com"
    cpf: str = "00011122233"


class ClienteDelSchema(BaseModel):
    """
    Define como deve ser a estrutura do dado retornado após uma requisição
    de remoção
    """
    message: str
    nome: str


def apresenta_cliente(cliente: Cliente):
    """
    Retorna uma representação do cliente seguindo o schema definido em
    ClienteViewSchema.
    """
    return {
        "id": cliente.id,
        "nome": cliente.nome,
        "telefone": cliente.telefone,
        "email": cliente.email,
        "cpf": cliente.cpf
    }
