# IMPORTS RELACIONADOS AO BANCO E MODELO
from typing import Optional
from sqlmodel import SQLModel, Field, create_engine, Session, select

# --- CONFIGURAÇÃO DO BANCO DE DADOS  ---
sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

# --- MODELO DE DADOS ---
class Cliente(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str
    idade: int
    tempo_cadastro: int
    username: str
    password: str
