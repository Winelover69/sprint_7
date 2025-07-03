# tests/test_create_courier.py
import pytest
import requests
import allure
from urls import COURIER_CREATE_URL
from courier_generator import generate_random_string, register_new_courier, login_courier, delete_courier


@allure.suite("API тесты: Создание курьера")
class TestCreateCourier:

    @allure.title("Успешное создание курьера: статус 201 и 'ok':true")
    @allure.description("Проверяем, что курьера можно создать, и запрос возвращает 201 и {'ok': true}")
    def test_create_courier_success(self, unique_courier_credentials):
        login = unique_courier_credentials["login"]
        password = unique_courier_credentials["password"]
        first_name = unique_courier_credentials["firstName"]

        with allure.step("Отправляем запрос на создание курьера"):
            response = register_new_courier(login, password, first_name)

        with allure.step("Проверяем код ответа и тело ответа"):
            assert response.status_code == 201
            assert response.json().get("ok") is True

        # Важно: После проверки успешного создания, мы получаем ID курьера
        # и удаляем его. Это можно сделать прямо здесь, если нет общей фикстуры,
        # которая бы занималась этим за нас.
        # В данном случае, мы должны убедиться, что курьер удален,
        # чтобы он не мешал будущим тестам.
        with allure.step("Очистка: получаем ID курьера и удаляем его"):
            courier_id = login_courier(login, password)
            assert courier_id is not None, "Не удалось получить ID созданного курьера для очистки."
            assert delete_courier(courier_id), f"Не удалось удалить курьера с ID: {courier_id}"

    @allure.title("Невозможно создать двух одинаковых курьеров")
    @allure.description("Проверяем, что при попытке создать курьера с существующим логином возвращается ошибка 409")
    def test_create_duplicate_courier_fails(self, created_courier_and_cleanup):
        # created_courier_and_cleanup уже создал курьера и обеспечит его удаление.
        # Используем логин этого уже созданного курьера для попытки дублирования.
        existing_login = created_courier_and_cleanup["login"]

        payload = {
            "login": existing_login,
            "password": generate_random_string(10),  # Пароль может быть другим
            "firstName": generate_random_string(10)  # Имя может быть другим
        }
        with allure.step("Отправляем запрос на создание дубликата курьера"):
            response = requests.post(COURIER_CREATE_URL, data=payload)

        with allure.step("Проверяем код ответа и тело ответа"):
            assert response.status_code == 409
            assert response.json().get("message") == "Этот логин уже используется. Попробуйте другой."

    @allure.title("Нельзя создать курьера без обязательных полей")
    @allure.description("Проверяем, что запрос без логина или пароля возвращает ошибку 400")
    @pytest.mark.parametrize("missing_field", ["login", "password"])
    def test_create_courier_without_required_field_fails(self, missing_field, unique_courier_credentials):
        # Используем уникальные данные, чтобы не получить конфликт логинов
        payload = {
            "login": unique_courier_credentials["login"],
            "password": unique_courier_credentials["password"],
            "firstName": unique_courier_credentials["firstName"]
        }
        payload.pop(missing_field)  # Удаляем одно из обязательных полей

        with allure.step(f"Отправляем запрос на создание курьера без поля '{missing_field}'"):
            response = requests.post(COURIER_CREATE_URL, data=payload)

        with allure.step("Проверяем код ответа и тело ответа"):
            assert response.status_code == 400
            assert response.json().get("message") == "Недостаточно данных для создания учетной записи"
        # Здесь нет необходимости в очистке, так как курьер не должен быть создан,
        # и тест ожидает ошибку.

    @allure.title("Можно создать курьера без необязательного поля firstName")
    @allure.description("Проверяем, что запрос без firstName возвращает 201 и {'ok': true}")
    def test_create_courier_without_firstname_success(self, unique_courier_credentials):
        login = unique_courier_credentials["login"]
        password = unique_courier_credentials["password"]
        # firstName отсутствует в payload

        payload = {
            "login": login,
            "password": password
        }

        with allure.step("Отправляем запрос на создание курьера без firstName"):
            response = requests.post(COURIER_CREATE_URL, data=payload)

        with allure.step("Проверяем код ответа и тело ответа"):
            assert response.status_code == 201
            assert response.json().get("ok") is True

        # Очистка данных после теста
        with allure.step("Очистка: получаем ID курьера и удаляем его"):
            courier_id = login_courier(login, password)
            assert courier_id is not None, "Не удалось получить ID созданного курьера для очистки."
            assert delete_courier(courier_id), f"Не удалось удалить курьера с ID: {courier_id}"

    @allure.title("Ошибка: создание курьера с логином, который уже есть")
    @allure.description("Проверяем, что если создать пользователя с логином, который уже есть, возвращается ошибка 409")
    def test_create_courier_with_existing_login_fails(self, created_courier_and_cleanup):
        # created_courier_and_cleanup уже создал курьера и обеспечит его удаление.
        # Используем логин этого уже созданного курьера для попытки дублирования.
        existing_login = created_courier_and_cleanup["login"]

        payload = {
            "login": existing_login,
            "password": generate_random_string(10),
            "firstName": generate_random_string(10)
        }
        with allure.step(f"Отправляем запрос на создание курьера с уже существующим логином '{existing_login}'"):
            response = requests.post(COURIER_CREATE_URL, data=payload)

        with allure.step("Проверяем код ответа и тело ответа"):
            assert response.status_code == 409
            assert response.json().get("message") == "Этот логин уже используется. Попробуйте другой."