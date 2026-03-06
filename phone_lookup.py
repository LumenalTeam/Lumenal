import phonenumbers
from phonenumbers import geocoder, carrier
from rich.panel import Panel

def lookup(number):
    try:
        # Парсим номер. Он сам поймет код страны (+1, +7, +44 и т.д.)
        parsed_number = phonenumbers.parse(number)
        
        # 1. Получаем локацию (на русском, если есть, иначе на английском)
        location = geocoder.description_for_number(parsed_number, "ru")
        if not location:
            location = geocoder.description_for_number(parsed_number, "en")
        
        # 2. Получаем оператора (Carrier)
        service_provider = carrier.name_for_number(parsed_number, "ru")
        if not service_provider:
            service_provider = carrier.name_for_number(parsed_number, "en")

        # 3. Определяем тип номера (мобильный, стационарный и т.д.)
        # Это поможет понять, стоит ли искать его в мессенджерах
        from phonenumbers import number_type
        ntype = phonenumbers.number_type(parsed_number)
        
        res = (
            f"[bold cyan]Страна/Регион:[/bold cyan] {location}\n"
            f"[bold cyan]Оператор:[/bold cyan] {service_provider if service_provider else 'Данные не найдены'}\n"
            f"[bold cyan]Тип связи:[/bold cyan] {ntype}\n\n"
            f"[bold yellow]Ссылки для OSINT:[/bold yellow]\n"
            f"• Telegram: https://t.me/{number.replace('+', '')}\n"
            f"• WhatsApp: https://wa.me/{number.replace('+', '')}\n"
            f"• Google: https://www.google.com/search?q=%22{number}%22"
        )
        return Panel(res, title=f"Анализ международного номера {number}", expand=False)
    
    except Exception as e:
        return f"[red]Ошибка формата! Убедитесь, что номер начинается с '+' (например, +1...)[/red]"