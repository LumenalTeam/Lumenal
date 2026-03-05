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

# 1. System Initialization
console = Console()
ua = UserAgent()

# 2. Target Data Sources
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