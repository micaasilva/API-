# Projeto: API de Gestão de Clientes (FastAPI + SQLModel) 


Este projeto consiste em uma API REST para gestão de clientes e um cliente interativo via terminal.

##  Como rodar o projeto

1. Instale as dependências:
   `pip install -r requirements.txt`

2. Inicie o servidor:
   `uvicorn server.main:app --reload`

3. Em outro terminal, rode o cliente:
   `python clientes/cliente.py`

## Tecnologias Utilizadas
- **FastAPI**: Framework da API.
- **SQLModel & SQLite**: Banco de dados relacional.
- **Rich**: Interface visual no terminal.
- **Requests**: Comunicação Cliente-Servidor.


