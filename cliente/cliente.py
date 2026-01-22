import requests
import sys
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, IntPrompt

# Configurações
BASE_URL = "http://127.0.0.1:8000"
console = Console()

def verificar_servidor():
    try:
        response = requests.get(f"{BASE_URL}/")
        return response.status_code == 200
    except requests.ConnectionError:
        return False

def exibir_menu():
    console.print(Panel.fit(
        "[bold blue]SISTEMA DE GESTÃO DE CLIENTES[/bold blue]\n"
        "[1] Listar Todos os Clientes\n"
        "[2] Buscar Cliente por ID\n"
        "[3] Ver Cliente Mais Antigo\n"
        "[4] Cadastrar Novo Cliente\n"
        "[5] Atualizar Dados de Cliente\n"
        "[6] Remover Cliente\n"
        "[0] Sair",
        title="Menu Principal", border_style="green"
    ))