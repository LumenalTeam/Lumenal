import socket
from rich.console import Console
from rich.table import Table

console = Console()

def scan_ports(host):
    # Список самых важных портов
    common_ports = {
        21: "FTP", 22: "SSH", 80: "HTTP", 
        443: "HTTPS", 3306: "MySQL", 3389: "RDP"
    }
    
    table = Table(title=f"Результаты сканирования {host}")
    table.add_column("Порт", style="cyan")
    table.add_column("Статус", style="bold magenta")
    table.add_column("Служба", style="green")

    console.print(f"[yellow]Начинаю сканирование (это может занять время)...[/yellow]")

    for port, service in common_ports.items():
        # Создаем "щуп" для проверки порта
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1) # Ждем ответ не больше 1 секунды
        result = s.connect_ex((host, port)) # 0 - порт открыт
        
        if result == 0:
            table.add_row(str(port), "ОТКРЫТ", service)
        s.close()
    
    console.print(table)