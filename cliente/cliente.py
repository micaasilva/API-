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

def listar_clientes():
    response = requests.get(f"{BASE_URL}/clientes")
    if response.status_code == 200:
        clientes = response.json()
        if not clientes:
            console.print("[yellow]Nenhum cliente cadastrado.[/yellow]")
            return
        
        table = Table(title="Lista de Clientes")
        table.add_column("ID", style="cyan")
        table.add_column("Nome", style="magenta")
        table.add_column("Idade", justify="right")
        table.add_column("Tempo (Meses)", justify="right")
        table.add_column("Usuário", style="green")

        for c in clientes:
            table.add_row(str(c['id']), c['nome'], str(c['idade']), str(c['tempo_cadastro']), c['username'])
        
        console.print(table)
    else:
        console.print("[red]Erro ao buscar clientes.[/red]")

def buscar_por_id():
    id_cliente = IntPrompt.ask("Digite o ID do cliente")
    response = requests.get(f"{BASE_URL}/clientes/{id_cliente}")
    if response.status_code == 200:
        c = response.json()
        console.print(Panel(
            f"[bold]Nome:[/bold] {c['nome']}\n"
            f"[bold]Idade:[/bold] {c['idade']}\n"
            f"[bold]Tempo de Cadastro:[/bold] {c['tempo_cadastro']} meses\n"
            f"[bold]Username:[/bold] {c['username']}",
            title=f"Dados do Cliente {id_cliente}", border_style="blue"
        ))
    else:
        console.print(f"[red]Cliente com ID {id_cliente} não encontrado.[/red]")

def ver_mais_antigo():
    response = requests.get(f"{BASE_URL}/clientes/mais-antigo")
    if response.status_code == 200:
        c = response.json()
        console.print(Panel(
            f"[bold]Nome:[/bold] {c['nome']}\n"
            f"[bold]Tempo:[/bold] {c['tempo_cadastro']} meses",
            title="🏆 Cliente Mais Antigo", border_style="yellow"
        ))
    else:
        console.print("[red]Erro ou nenhum cliente cadastrado.[/red]")