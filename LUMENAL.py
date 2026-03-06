import asyncio
import aiohttp
import time
import os
from rich.console import Console
from rich.table import Table
from rich.text import Text
from fake_useragent import UserAgent
from rich.align import Align
from rich.panel import Panel
import webbrowser
import metadata_engine
import network_tools
import requests
import port_scanner
from rich.progress import track
console = Console()
import random
import phone_lookup

AGENTS = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
    ]
def get_headers():
    return {"User-Agent": random.choice(AGENTS)}
# 1. Target Data Sources
SITES = [
    # Social & General
    ("VK", "https://vk.com/{}", "404 Not Found"),
    ("GitHub", "https://github.com/{}", "Not Found"),
    ("Twitch", "https://www.twitch.tv/{}", "is not available"),
    ("Telegram", "https://t.me/{}", "If you have Telegram, you can contact"),
    ("TikTok", "https://www.tiktok.com/@{}", "Couldn't find this account"),
    ("YouTube", "https://www.youtube.com/@{}", "404"),
    ("Reddit", "https://www.reddit.com/user/{}", "404 Not Found"),
    ("Pinterest", "https://www.pinterest.com/{}/", "User not found"),
    ("Instagram", "https://www.instagram.com/{}/", "Page Not Found"),
    
    # Gaming
    ("Steam", "https://steamcommunity.com/id/{}", "The specified profile could not be found"),
    ("Roblox", "https://www.roblox.com/user.aspx?username={}", "Page Not Found"),
    ("Minecraft", "https://api.mojang.com/users/profiles/minecraft/{}", "error"),
    ("Chess.com", "https://www.chess.com/member/{}", "404"),
    ("osu!", "https://osu.ppy.sh/users/{}", "404"),
    ("Battle.net", "https://overwatch.stat.io/profile/pc/global/{}", "Not Found"),
    
    # Tech & Creative
    ("Habr", "https://habr.com/ru/users/{}/", "404"),
    ("Pikabu", "https://pikabu.ru/@{}", "404"),
    ("DeviantArt", "https://www.deviantart.com/{}", "404 Not Found"),
    ("SoundCloud", "https://soundcloud.com/{}", "404 Not Found"),
    ("Behance", "https://www.behance.net/{}", "404"),
    
    # Forums & Communities
    ("Discord.me", "https://discord.me/{}", "404"),
    ("Letterboxd", "https://letterboxd.com/{}/", "404"),
    ("Archive.org", "https://archive.org/details/@{}", "404"),
    ("Replit", "https://replit.com/@{}", "404"),
    ("Linktree", "https://linktr.ee/{}", "404")
]
def main_menu():
    print("\n" + "="*30)
    print("      LUMENAL OSINT TOOL")
    print("="*30)
    print("[1] Nickname Search (Social Media)")
    print("[2] Email Leack Checker(Data Breaches)")
    print("[3] Metadata Analyzer (Images)")
    print("[4] IP Lookup (Geolocation):")
    print("[5] Port Scanner (Network):")
    print("[6] Phone Lookup (International):")
    print("[0] Exit")
    
    choice = input("\nSelect an option: ")
    return choice

def check_leak():
    email = input("\n[?] Enter email to check: ").strip()
    
    if not email:
        console.print("[bold red][!] You didn't enter anything![/bold red]")
        return

    console.print(f"[bold yellow][!] Checking databases for: {email}[/bold yellow]")
    
    leak_url = f"https://leakcheck.io/search?type=email&check={email}"
    
    console.print(Panel(
        f"[bold green][+] Search link generated successfully.[/bold green]\n"
        f"[white]Follow this link to see results:[/white]\n"
        f"[bold cyan]{leak_url}[/bold cyan]",
        title="Leak Report",
        expand=False
    ))
    
    try:
        headers = {"User-Agent": random.choice(AGENTS)}
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get("found", 0) > 0:
                console.print(f"[bold red][!] WARNING: Found in {data['found']} data breaches![/bold red]")
                console.print("[white]Recommendation: Change your password immediately.[/white]")
            else:
                console.print("[bold green][+] No leaks found in public databases.[/bold green]")
        else:
            console.print(f"[bold cyan][*] Visit: https://haveibeenpwned.com/unifiedsearch/{email}[/bold cyan]")
    except:
        console.print("[red][!] Connection error. Please try again later.[/red]")

def nickname_search():
    nick = input("\n[?] Enter nickname: ")
    found_count = 0
    
    
    
    user_proxy = None 
    proxies = {"http": user_proxy, "https": user_proxy} if user_proxy else None

    for name, url_template, error_text in track(SITES, description="Scanning..."):
        url = url_template.format(nick)
        try:
            
            response = requests.get(
                url, 
                headers=get_headers(), 
                proxies=proxies, 
                timeout=7
            )
            
            if response.status_code == 200 and error_text not in response.text:
                console.print(f"[bold green][+] Found on {name}:[/bold green] {url}")
        except Exception:
            continue
            
    console.print(f"\n[bold cyan]Готово! Найдено активных аккаунтов: {found_count}[/bold cyan]")

while True:
    user_choice = main_menu()
    
    if user_choice == '1':
        nickname_search()
    elif user_choice == '2':
        # 1. Получаем ввод
        email = input("\n[?] Enter email: ").strip()
        
        # 2. Создаем переменную (назовем её просто url, чтобы не путаться)
        url = f"https://intelx.io/?s={email}"
        
        # 3. Выводим её. ВАЖНО: имя в {} должно совпадать с именем выше!
        console.print(Panel(
            f"[bold green][+] Result for {email}:[/bold green]\n"
            f"[bold cyan]{url}[/bold cyan]",
            title="Data Breach Search",
            expand=False
        ))
        
        # Чтобы меню не улетало сразу вверх
        input("\nPress Enter to continue...")
    elif user_choice == '3':
        path = input("Drag and drop photo to console: ").strip("'\"")
        metadata_engine.get_exif_data(path)
    elif user_choice == '4':
        import network_tools
        ip_to_check = input("Enter IP for analysis: ")
        network_tools.get_ip_info(ip_to_check)
    elif user_choice == '5':
        import port_scanner
        target_host = input("Enter domain or IP for scanning: ")
        port_scanner.scan_ports(target_host)
    elif user_choice == '6':
     import phone_lookup
     phone = input("Enter phonenumber(e.g. +1...): ")
     result = phone_lookup.lookup(phone)
     console.print(result)
    elif user_choice == '0':
        print("Exiting system...")
        break
    else:
        print("Error! PLease select an option from 0 to 6.")

# 2. System Initialization
ua = UserAgent()

# 3. Visual Identity
def clear_and_logo():
    os.system('cls' if os.name == 'nt' else 'clear')
    
   
    banner_text = Text("L U M E N A L", style="bold yellow")
   
    sub_text = Text("\nOSINT FRAMEWORK • STEALTH EDITION • V1.0", style="dim white")
    
    header_content = Text.assemble(banner_text, sub_text)
    
    
    console.print(
        Panel(
            Align.center(header_content),
            border_style="yellow",
            padding=(1, 2),
            title="[bold white] CORE SYSTEM [/bold white]",
            subtitle="[bold green] ONLINE [/bold green]"
        )
    )
    
    
    status = Text()
    status.append(" > READY TO SCAN", style="bold green")
    status.append(" | DATABASE: 25 SITES", style="bold white")
    
    console.print(status, justify="center")
    
    console.print(f"[dim white]{'—' * console.width}[/dim white]")



# 4. Asynchronous Core Logic
async def check_site(session, name, template, error_msg, username):
    url = template.format(username)
    headers = {'User-Agent': ua.random}
    try:
        async with session.get(url, headers=headers, timeout=8) as response:
            text = await response.text()
            if response.status == 200 and error_msg.lower() not in text.lower():
                return (username, name, url)
    except:
        pass
    return None

async def run_lumenal_scan(nick):
    connector = aiohttp.TCPConnector(limit_per_host=5)
    async with aiohttp.ClientSession(connector=connector) as session:
        tasks = [check_site(session, n, t, e, nick) for n, t, e in SITES]
        results = await asyncio.gather(*tasks)
        return [r for r in results if r]

# 5. Data Exporting
def save_report(target_username, found_data):
    try:
        filename = f"lumenal_report_{target_username}.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"LUMENAL DISCOVERY LOG | {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"IDENTIFIER: {target_username}\n")
            f.write("-" * 45 + "\n")
            for r in found_data:
                f.write(f"[+] {r[1]}: {r[2]}\n")
        return filename
    except:
        return None

# 6. Main Execution Block
async def main():
    clear_and_logo()
    target = console.input("[bold yellow][>] TARGET_ID: [/bold yellow]").strip()
    
    if not target:
        console.print("[red][!] ERROR: NULL_INPUT[/red]")
        return

    console.print(f"[*] INITIALIZING LUMENAL SCAN: {target}...")

    found = await run_lumenal_scan(target)
    
    if found:
        table = Table(title=f"\n[bold yellow]LUMENAL_RESULTS[/bold yellow]", header_style="bold yellow", border_style="dim white")
        table.add_column("SOURCE", style="white")
        table.add_column("ENDPOINT", style="yellow")
        
        for r in found:
            table.add_row(r[1], r[2])
        
        console.print(table)
        
        report_file = save_report(target, found)
        if report_file:
            console.print(f"\n[bold green][SUCCESS][/bold green] LOG_EXPORTED: {report_file}")
    else:
        console.print(f"\n[bold red][FAILURE][/bold red] DATA_NOT_FOUND")

    console.input("\n[dim white]TERMINATE SESSION (ENTER)...[/dim white]")

# 7. Entry Point
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass