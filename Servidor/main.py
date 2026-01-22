# IMPORTS RELACIONADOS AO BANCO E MODELO
from typing import Optional
from sqlmodel import SQLModel, Field, create_engine, Session, select
from typing import List
from fastapi import FastAPI, HTTPException, Depends
from sqlmodel import Session, select
from fastapi import HTTPException, status, Depends
from sqlmodel import Session

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

app = FastAPI(
    title="Sistema de Vendas - API de Gestão de Clientes",
    description="API desenvolvida para o projeto do 2º Bimestre.",
    version="1.0.0"
)

# --- INICIALIZAÇÃO DA API ---
@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# --- ROTAS DE LEITURA (Pessoa C) ---

@app.get("/")
def read_root():
    return {"status": "online"}

@app.get("/clientes", response_model=List[Cliente])
def listar_clientes(session: Session = Depends(get_session)):
    return session.exec(select(Cliente)).all()

@app.get("/clientes/mais-antigo", response_model=Cliente)
def cliente_mais_antigo(session: Session = Depends(get_session)):
    cliente = session.exec(
        select(Cliente).order_by(Cliente.tempo_cadastro.desc())
    ).first()

    if not cliente:
        raise HTTPException(status_code=404, detail="Nenhum cliente cadastrado")
    return cliente

@app.get("/clientes/{cliente_id}", response_model=Cliente)
def buscar_cliente(cliente_id: int, session: Session = Depends(get_session)):
    cliente = session.get(Cliente, cliente_id)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return cliente
# --- ROTAS DE ESCRITA E MODIFICAÇÃO (Pessoa B) ---

@app.post("/clientes", response_model=Cliente, status_code=status.HTTP_201_CREATED)
def criar_cliente(cliente: Cliente, session: Session = Depends(get_session)):
    session.add(cliente)
    session.commit()
    session.refresh(cliente)
    return cliente

@app.patch("/clientes/{cliente_id}", response_model=Cliente)
def atualizar_cliente(cliente_id: int, dados_atualizacao: dict, session: Session = Depends(get_session)):
    cliente = session.get(Cliente, cliente_id)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")

    for key, value in dados_atualizacao.items():
        if hasattr(cliente, key):
            setattr(cliente, key, value)

    session.commit()
    session.refresh(cliente)
    return cliente

@app.delete("/clientes/{cliente_id}")
def remover_cliente(cliente_id: int, session: Session = Depends(get_session)):
    cliente = session.get(Cliente, cliente_id)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")

    session.delete(cliente)
    session.commit()
    return {"message": "Cliente removido com sucesso"}
