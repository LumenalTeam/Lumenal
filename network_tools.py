import requests
from rich.panel import Panel

def get_ip_info(ip):
    print(f"\n[!] Устанавливаю соединение для анализа {ip}...")
    try:
        # Отправляем запрос к бесплатному API
        response = requests.get(f"http://ip-api.com/json/{ip}")
        data = response.json() # Переводим ответ из формата JSON в словарь Python
        
        if data['status'] == 'success':
            print("-" * 30)
            print(f"[*] IP:          {data.get('query')}")
            print(f"[*] СТРАНА:      {data.get('country')}")
            print(f"[*] ГОРОД:       {data.get('city')}")
            print(f"[*] ПРОВАЙДЕР:   {data.get('isp')}")
            print(f"[*] КООРДИНАТЫ:  {data.get('lat')}, {data.get('lon')}")
            print("-" * 30)
        else:
            print(f"[-] Ошибка: Сервер вернул статус '{data.get('status')}'")
            
    except Exception as e:
        print(f"[!] Ошибка: Не удалось получить данные. Проверь интернет или библиотеку requests.")
        print(f"Детали ошибки: {e}")