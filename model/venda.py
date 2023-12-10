from sqlalchemy import Column, String, Integer, DateTime, Float, ForeignKey
from datetime import datetime
from typing import Union
from sqlalchemy.orm import relationship

from model import Base, Produto, Cliente

class Venda(Base):
    __tablename__ = "venda"

    id = Column("pk_venda", Integer, primary_key=True)
    produto_id = Column("cod_produto", Integer, ForeignKey("produto.pk_produto"), nullable=False)
    produto = relationship("Produto", backref='venda', lazy=True)
    cliente_id = Column("cod_cliente", Integer, ForeignKey("cliente.pk_cliente"), nullable=False)
    cliente = relationship("Cliente", backref="venda", lazy=True)
    quantidade = Column(Integer)
    valor = Column(Float)
    data_venda = Column(DateTime, default=datetime.now())


    def __init__(self, produto:int, cliente:int, quantidade:int, valor:float, data_venda: Union[DateTime, None] = None):
        self.produto_id = produto
        self.cliente_id = cliente
        self.quantidade = quantidade
        self.valor = valor
        
        if data_venda:
            self.data_venda = data_venda

    def __repr__(self):
        return f"Produto_id = {self.produto_id}, Cliente_id = {self.cliente_id}, Quantidade = {self.quantidade}, valor = {self.valor}"