from pydantic import BaseModel
from typing import Optional, List
from model.venda import Venda
from model.cliente import Cliente
from model.produto import Produto

class VendaSchema(BaseModel):
    """
    Define como uma nova venda a ser inserida deverá ser apresentada
    """
    produto_id: int = 999
    cliente_id: int = 999
    quantidade: int = 99
    valor: float = 99.99


class VendaBuscaSchema(BaseModel):
    """
    Define como deve ser a estrutura que representa a busca. Que será
    feita apenas com base no id da venda.
    """
    id: int = 000
    

class ListagemVendasSchema(BaseModel):
    """
    Define como uma listagem de vendas será retornada.
    """
    vendas:List[VendaSchema]


def apresenta_vendas(vendas: List[Venda]):
    """
    Retorna uma apresentação da venda seguindo o schema definido em
    VendaViewSchema
    """
    result = []
    for venda in vendas:
        result.append({
            "id": venda.id,
            "produto": venda.produto_id,
            "cliente": venda.cliente_id,
            "quantidade": venda.quantidade,
            "valor": venda.valor,
            "data_venda": venda.data_venda
        })

    return {"vendas": result}


class VendaViewSchema(BaseModel):
    """
    Define como uma venda será retornada.
    """
    id: int = 999
    produto: int = 999
    cliente: int = 999
    quantidade: int = 999
    valor: float = 999.99


class VendaDelSchema(BaseModel):
    """
    Define como deve ser a estrutura do dado retornado após uma requisição
    de remoção
    """
    message: str
    id: str
    produto: str


def apresenta_venda(venda: Venda):
    """
    Retorna uma representação da venda seguindo o schema definido em
    VendaViewSchema.
    """
    return {
        "id": venda.id,
        "produto": venda.produto_id,
        "cliente": venda.cliente_id,
        "quantidade": venda.quantidade,
        "valor": venda.valor,
        "data_venda": venda.data_venda
    }