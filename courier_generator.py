import requests
import random
import string

# URL базового API
BASE_URL = "https://qa-scooter.praktikum-services.ru"

def generate_random_string(length):
    """Генерирует случайную строку заданной длины из букв нижнего регистра."""
    letters = string.ascii_lowercase
    random_string = ''.join(random.choice(letters) for i in range(length))
    return random_string

def register_new_courier(login, password, first_name):
    """
    Отправляет запрос на регистрацию нового курьера.
    Возвращает объект ответа (requests.Response).
    """
    payload = {
        "login": login,
        "password": password,
        "firstName": first_name
    }
    response = requests.post(f'{BASE_URL}/api/v1/courier', data=payload)
    return response

def login_courier(login, password):
    """
    Логинится курьером и возвращает его ID.
    Возвращает ID курьера (int) или None, если логин не удался.
    """
    payload = {
        "login": login,
        "password": password
    }
    response = requests.post(f'{BASE_URL}/api/v1/courier/login', data=payload)
    if response.status_code == 200:
        return response.json().get("id")
    return None

def delete_courier(courier_id):
    """
    Удаляет курьера по его ID.
    Возвращает True, если удаление успешно (статус 200 и ok:true), иначе False.
    """
    if courier_id: # Проверяем, что courier_id не None или 0
        response = requests.delete(f'{BASE_URL}/api/v1/courier/{courier_id}')
        return response.status_code == 200 and response.json().get("ok") == True
    return False # Если ID нет, считаем, что удаление не произошло