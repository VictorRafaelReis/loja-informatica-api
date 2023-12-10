from sqlalchemy import Column, String, Integer, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from model import Base

class Cliente(Base):
    __tablename__ = "cliente"

    id = Column("pk_cliente", Integer, primary_key=True)
    nome = Column(String(150))
    telefone = Column(String(11))
    email = Column(String(100))
    cpf = Column(String(11), unique=True)

    def __init__(self, nome:str, telefone:str, email:str, cpf:str):
        self.nome = nome
        self.telefone = telefone
        self.email = email
        self.cpf = cpf

    def __repr__(self):
        return self.cpf