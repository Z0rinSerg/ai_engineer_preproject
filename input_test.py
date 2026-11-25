import os
import getpass
from urllib.parse import quote

def main():
    # --- ВВОД ДАННЫХ ---
    print("Введите для прокси-сервера:")
    username = input("Имя пользователя [zorin_sv]: ").strip() or "zorin_sv" 
    domain = input("Название домена [d0]").strip() or "d0"
    # 1. Запрашиваем пароль без отображения
    password = getpass.getpass(prompt='Введите пароль для прокси-сервера: ')
    if not password:
        print("Ошибка: пароль не может быть пустым.")
        return
    encoded_password = quote(password, safe='')
    print(f" domain:{domain}\n username: {username}\n Пароль = {encoded_password}")








if __name__ == "__main__": 
    main()