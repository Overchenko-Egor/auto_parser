import parser.Credits
import requests
from bs4 import BeautifulSoup

def p_masuma(input_data):
    # Установите ваши учетные данные
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
        print("Форма логина не найдена. Проверьте HTML страницу.")
        exit()

    # Поиск скрытого токена
    csrf_token_input = login_form.find('input', {'name': '_csrf_token'})
    if csrf_token_input is None:
        print("Не удалось найти CSRF токен. Проверьте HTML страницу.")
        exit()

    # Поиск полей ввода для логина и пароля
    username_input = login_form.find('input', {'name': '_username'})
    password_input = login_form.find('input', {'name': '_password'})
    submit_button = login_form.find('button', {'type': 'submit'})

    # Проверка наличия необходимых элементов
    if username_input is None or password_input is None or submit_button is None:
        print("Не удалось найти необходимые поля формы. Проверьте HTML страницу.")
        exit()

    # Данные для авторизации
    login_data = {
        '_csrf_token': csrf_token_input['value'],
        '_username': username,
        '_password': password,
        '_remember_me': '1'  # Если нужно, чтобы пользователь остался авторизованным
    }

    # Заголовки (если требуется)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Referer': login_url
    }

    # Авторизация
    response = session.post(login_url, data=login_data, headers=headers)

    # Вывод статуса и текста ответа для отладки
    print(f"Статус код ответа: {response.status_code}")
    print("Текст ответа:", response.text)  # Выводим только первые 500 символов ответа

    # Проверка успешности авторизации
    if response.status_code == 200:
        if 'logout' in response.text.lower() or 'личный кабинет' in response.text.lower():
            print('Успешная авторизация')
        else:
            print('Ошибка авторизации. Проверьте данные и параметры.')
            if 'invalid' in response.text.lower():
                print("- Возможно, неверные учетные данные.")
            if 'csrf' in response.text.lower():
                print("- Проблема с CSRF токеном.")
            exit()
    else:
        print(f"Ошибка авторизации: {response.status_code}")
        exit()

    # Запрос данных после авторизации
    data_response = session.get(data_url)

    # Вывод статуса и текста ответа для отладки
    print(f"Статус код ответа на запрос данных: {data_response.status_code}")
    
    # Проверка успешности получения данных
    if data_response.status_code == 200:
        print("Успешно получены данные")
        soup = BeautifulSoup(data_response.content, 'html.parser')
        # Обработка данных, например:
        data = soup.find_all('div', class_='product-card-extended__wrapper')  # Убедитесь, что это правильный класс для данных
        if data:
            # for item in data:
                # print(item.text)
            
            session.close()
            return data
        else:
            print("Не удалось найти данные на странице.")
            session.close()
            return soup.find
    else:
        print(f"Ошибка получения данных: {data_response.status_code}")
        print(data_response.text[:500])  # Выводим только первые 500 символов ответа

    # Закрытие сессии
    session.close()
