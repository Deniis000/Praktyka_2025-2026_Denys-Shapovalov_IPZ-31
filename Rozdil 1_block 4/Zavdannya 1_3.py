import os
from dotenv import load_dotenv

load_dotenv()

# Зчитуємо змінні оточення. Якщо змінної немає, повертаємо значення за замовчуванням (None)
database_url = os.getenv('DB_URL')
api_key = os.getenv('API_KEY')
environment = os.getenv('APP_ENV', 'production')  # Значення за замовчуванням - 'production'

if not database_url or not api_key:
    print("Помилка: Необхідні змінні оточення DB_URL та API_KEY не встановлені!")
else:
    print("--- Конфігурація завантажена ---")
    print(f"Середовище: {environment}")
    # Маскуємо пароль
    print(f"DB URL: {database_url.replace(database_url.split(':')[2], '*****')}")
    # Виводимо лише частину ключа
    print(f"API Key: {api_key[:4]}...{api_key[-4:]}")