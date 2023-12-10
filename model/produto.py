from sqlalchemy import Column, String, Integer, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from model import Base

class Produto(Base):
    __tablename__ = "produto"

    id = Column("pk_produto", Integer, primary_key=True)
    nome = Column(String(150), unique=True)
    categoria = Column(String(50))
    quantidade = Column(Integer)
    valor = Column(Float)
    
    def __init__(self, nome:str, categoria:str, quantidade:int, valor:float):
        self.nome = nome
        self. categoria = categoria
        self.quantidade = quantidade
        self.valor = valor
    
    def __repr__(self):
        return self.nome