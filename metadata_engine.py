from PIL import Image
from PIL.ExifTags import TAGS

def get_exif_data(image_path):
    try:
        img = Image.open(image_path)
        info = img._getexif()
        
        print(f"\n--- Анализ метаданных: {image_path} ---")
        
        if info:
            found = False
            for tag, value in info.items():
                tag_name = TAGS.get(tag, tag)
                # Выводим самое интересное: камеру, дату, софт и GPS
                if tag_name in ['Make', 'Model', 'DateTime', 'Software', 'GPSInfo']:
                    print(f"[*] {tag_name:10}: {value}")
                    found = True
            if not found:
                print("[-] Основные теги не найдены, но файл содержит скрытые данные.")
        else:
            print("[-] Метаданные (EXIF) отсутствуют. Соцсети обычно их удаляют.")
            
    except Exception as e:
        print(f"[!] Ошибка при чтении файла: {e}")

# Это нужно для теста, потом удалим
if __name__ == "__main__":
    path = input("Перетащи фото в это окно и нажми Enter: ").strip('"')
    get_exif_data(path)
