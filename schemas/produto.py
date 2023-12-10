from pydantic import BaseModel
from typing import Optional, List
from model.produto import Produto

class ProdutoSchema(BaseModel):
    """
    Define como um novo produto a ser inserido deverá ser apresentado
    """
    nome: str = "Nome do Produto"
    categoria: str = "Hardware/Software"
    quantidade: Optional[int] = 99
    valor: float = 99.99


class ProdutoBuscaSchema(BaseModel):
    """
    Define como deve ser a estrutura que representa a busca. Que será
    feita apenas com base no nome do produto.
    """
    nome: str = "Nome do produto"

class ProdutoBuscaPorIdSchema(BaseModel):
    """
    Define como deve ser a estrutura que representa a busca. Que será
    feita apenas com base no id do produto.
    """
    id: int = 1

class ListagemProdutosSchema(BaseModel):
    """
    Define como uma listagem de produtos será retornada.
    """
    produtos:List[ProdutoSchema]


def apresenta_produtos(produtos: List[Produto]):
    """
    Retorna uma apresentação do produto seguindo o schema definido em
    ProdutoViewSchema
    """
    result = []
    for produto in produtos:
        result.append({
            "id": produto.id,
            "nome": produto.nome,
            "categoria": produto.categoria,
            "quantidade": produto.quantidade,
            "valor": produto.valor
        })

    return {"produtos": result}


class ProdutoViewSchema(BaseModel):
    """
    Define como um produto será retornado.
    """
    id: int = 999
    nome: str = "Algum Nome de Produto"
    categoria: str = "Hardware/Software"
    quantidade: Optional[int] = 99
    valor: float = 999.99


class ProdutoDelSchema(BaseModel):
    """
    Define como deve ser a estrutura do dado retornado após uma requisição
    de remoção
    """
    message: str
    nome: str


def apresenta_produto(produto: Produto):
    """
    Retorna uma representação do produto seguindo o schema definido em
    ProdutoViewSchema.
    """
    return {
        "id": produto.id,
        "nome": produto.nome,
        "categoria": produto.categoria,
        "quantidade": produto.quantidade,
        "valor": produto.valor
    }
