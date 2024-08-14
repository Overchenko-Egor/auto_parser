import parser.Credits
import requests
from bs4 import BeautifulSoup


def p_masuma(input_data):
    # Учетные данные
    username = parser.Credits.masuma.login
    password = parser.Credits.masuma.password

    # URLs
    login_url = 'https://masuma.ru/login'
    data_url = 'https://masuma.ru/search?query=' + input_data

    # Создание сессии
    session = requests.Session()

    # Получение страницы логина
    login_page = session.get(login_url)
    login_soup = BeautifulSoup(login_page.content, 'html.parser')

    # Поиск формы логина
    login_form = login_soup.find('form', {'class': 'authorization-form'})
    if login_form is None:
        print("Форма логина не найдена.")
        session.close()
        return None

    # Поиск скрытого токена CSRF
    csrf_token_input = login_form.find('input', {'name': '_csrf_token'})
    if csrf_token_input is None:
        print("Не найден CSRF токен.")
        session.close()
        return None

    # Данные для авторизации
    login_data = {
        '_csrf_token': csrf_token_input['value'],
        '_username': username,
        '_password': password,
        '_remember_me': '1'
    }

    # Заголовки
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Referer': login_url
    }

    # Выполнение запроса на авторизацию
    response = session.post(login_url, data=login_data, headers=headers)

    # Проверка успешности авторизации
    if response.status_code == 200 and ('logout' in response.text.lower() or 'личный кабинет' in response.text.lower()):
        print('Успешная авторизация')
        print (response.text)
        print ()
        print ()
        print ()
        print ()
    else:
        print('Ошибка авторизации или неверные учетные данные.')
        session.close()
        return None

    # Запрос данных после авторизации
    data_response = session.get(data_url, headers=headers, cookies=session.cookies)

    # Проверка успешности получения данных
    if data_response.status_code == 200:
        soup = BeautifulSoup(data_response.content, 'html.parser')

        # Пример поиска данных
        data = soup.find_all('div', class_='product-card-extended__wrapper')

        if data:
            session.close()
            return data
        else:
            print("Не удалось найти данные на странице.")
            session.close()
            return None
    else:
        print(f"Ошибка получения данных: {data_response.status_code}")
        session.close()
        return None