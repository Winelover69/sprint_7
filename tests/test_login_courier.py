import pytest
import requests
import allure
from urls import COURIER_LOGIN_URL
from courier_generator import register_new_courier_and_return_login_password, login_courier, delete_courier


@allure.suite("API тесты: Логин курьера")
class TestLoginCourier:

    @allure.title("Успешный логин курьера")
    @allure.description("Проверяем, что курьер может авторизоваться и запрос возвращает ID")
    def test_login_courier_success(self, new_courier_data):
        payload = {
            "login": new_courier_data["login"],
            "password": new_courier_data["password"]
        }
        with allure.step("Отправляем запрос на логин курьера"):
            response = requests.post(COURIER_LOGIN_URL, data=payload)

        with allure.step("Проверяем код ответа и тело ответа"):
            assert response.status_code == 200
            assert "id" in response.json()
            assert response.json()["id"] is not None

    @allure.title("Нельзя залогиниться с неправильным логином")
    @allure.description("Проверяем, что при неправильном логине возвращается ошибка 404")
    def test_login_courier_with_wrong_login_fails(self, new_courier_data):
        payload = {
            "login": "wrong_login",  # Неправильный логин
            "password": new_courier_data["password"]
        }
        with allure.step("Отправляем запрос на логин с неправильным логином"):
            response = requests.post(COURIER_LOGIN_URL, data=payload)

        with allure.step("Проверяем код ответа и тело ответа"):
            assert response.status_code == 404
            assert response.json().get("message") == "Учетная запись не найдена"

    @allure.title("Нельзя залогиниться с неправильным паролем")
    @allure.description("Проверяем, что при неправильном пароле возвращается ошибка 404")
    def test_login_courier_with_wrong_password_fails(self, new_courier_data):
        payload = {
            "login": new_courier_data["login"],
            "password": "wrong_password"  # Неправильный пароль
        }
        with allure.step("Отправляем запрос на логин с неправильным паролем"):
            response = requests.post(COURIER_LOGIN_URL, data=payload)

        with allure.step("Проверяем код ответа и тело ответа"):
            assert response.status_code == 404
            assert response.json().get("message") == "Учетная запись не найдена"

    @allure.title("Нельзя залогиниться без обязательных полей")
    @allure.description("Проверяем, что запрос без логина или пароля возвращает ошибку 400")
    @pytest.mark.parametrize("missing_field", ["login", "password"])
    def test_login_courier_without_required_field_fails(self, missing_field, new_courier_data):
        payload = {
            "login": new_courier_data["login"],
            "password": new_courier_data["password"]
        }
        payload.pop(missing_field)  # Удаляем одно из обязательных полей

        with allure.step(f"Отправляем запрос на логин без поля '{missing_field}'"):
            response = requests.post(COURIER_LOGIN_URL, data=payload)

        with allure.step("Проверяем код ответа и тело ответа"):
            assert response.status_code == 400
            assert response.json().get("message") == "Недостаточно данных для входа"

    @allure.title("Нельзя залогиниться под несуществующим пользователем")
    @allure.description("Проверяем, что логин несуществующим пользователем возвращает ошибку 404")
    def test_login_non_existent_courier_fails(self):
        payload = {
            "login": "nonexistent_login_123",
            "password": "nonexistent_password_123"
        }
        with allure.step("Отправляем запрос на логин несуществующего курьера"):
            response = requests.post(COURIER_LOGIN_URL, data=payload)

        with allure.step("Проверяем код ответа и тело ответа"):
            assert response.status_code == 404
            assert response.json().get("message") == "Учетная запись не найдена"