import requests
import random
import string

# URL базового API
BASE_URL = "https://qa-scooter.praktikum-services.ru"

# метод регистрации нового курьера возвращает список из логина и пароля и имени
# если регистрация не удалась, возвращает пустой список
def register_new_courier_and_return_login_password():
    # метод генерирует строку, состоящую только из букв нижнего регистра, в качестве параметра передаём длину строки
    def generate_random_string(length):
        letters = string.ascii_lowercase
        random_string = ''.join(random.choice(letters) for i in range(length))
        return random_string

    # создаём список, чтобы метод мог его вернуть
    login_pass_name = []

    # генерируем логин, пароль и имя курьера
    login = generate_random_string(10)
    password = generate_random_string(10)
    first_name = generate_random_string(10)

    # собираем тело запроса
    payload = {
        "login": login,
        "password": password,
        "firstName": first_name
    }

    # отправляем запрос на регистрацию курьера и сохраняем ответ в переменную response
    response = requests.post(f'{BASE_URL}/api/v1/courier', data=payload)

    # если регистрация прошла успешно (код ответа 201), добавляем в список логин, пароль и имя курьера
    if response.status_code == 201:
        login_pass_name.append(login)
        login_pass_name.append(password)
        login_pass_name.append(first_name)

    # возвращаем список
    return login_pass_name

def login_courier(login, password):
    "Логинится курьером и возвращает его ID."
    payload = {
        "login": login,
        "password": password
    }
    response = requests.post(f'{BASE_URL}/api/v1/courier/login', data=payload)
    if response.status_code == 200:
        return response.json().get("id")
    return None

def delete_courier(courier_id):
    "Удаляет курьера по его ID."
    if courier_id:
        response = requests.delete(f'{BASE_URL}/api/v1/courier/{courier_id}')
        return response.status_code == 200 and response.json().get("ok") == True
    return False