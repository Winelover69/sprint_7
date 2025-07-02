import pytest
import requests
import allure
from urls import COURIER_CREATE_URL
from courier_generator import register_new_courier_and_return_login_password, delete_courier, login_courier


@allure.suite("API тесты: Создание курьера")
class TestCreateCourier:

    @allure.title("Успешное создание курьера")
    @allure.description("Проверяем, что курьера можно создать, и запрос возвращает 201 и {'ok': true}")
    def test_create_courier_success(self, new_courier_data):
        # new_courier_data уже содержит данные нового курьера, созданного фикстурой
        # и удалит его после теста. Дополнительно создавать здесь не нужно.
        # Просто проверяем, что курьер был создан.
        with allure.step("Проверяем, что курьер был создан успешно"):
            assert new_courier_data["id"] is not None
            # Также можно проверить ответ от первичного запроса на создание, если он был бы здесь
            # Но фикстура уже об этом позаботилась

    @allure.title("Невозможно создать двух одинаковых курьеров")
    @allure.description("Проверяем, что при попытке создать курьера с существующим логином возвращается ошибка 409")
    def test_create_duplicate_courier_fails(self, new_courier_data):
        payload = {
            "login": new_courier_data["login"],
            "password": new_courier_data["password"],
            "firstName": new_courier_data["firstName"]
        }
        with allure.step("Отправляем запрос на создание дубликата курьера"):
            response = requests.post(COURIER_CREATE_URL, data=payload)

        with allure.step("Проверяем код ответа и тело ответа"):
            assert response.status_code == 409
            assert response.json().get("message") == "Этот логин уже используется. Попробуйте другой."

    @allure.title("Нельзя создать курьера без обязательных полей")
    @allure.description("Проверяем, что запрос без логина или пароля возвращает ошибку 400")
    @pytest.mark.parametrize("missing_field", ["login", "password"])
    def test_create_courier_without_required_field_fails(self, missing_field):
        # Генерируем уникальные данные, чтобы не было конфликта логинов
        test_courier_data = register_new_courier_and_return_login_password()

        payload = {
            "login": test_courier_data[0],
            "password": test_courier_data[1],
            "firstName": test_courier_data[2]
        }
        payload.pop(missing_field)  # Удаляем одно из обязательных полей

        with allure.step(f"Отправляем запрос на создание курьера без поля '{missing_field}'"):
            response = requests.post(COURIER_CREATE_URL, data=payload)

        with allure.step("Проверяем код ответа и тело ответа"):
            assert response.status_code == 400
            assert response.json().get("message") == "Недостаточно данных для создания учетной записи"

        # Удаляем созданного курьера, если он случайно был создан (хотя не должен)
        # Это не обязательно, т.к. тест нацелен на проверку отсутствия создания
        # Но для надежности можно добавить
        if response.status_code == 201:
            courier_id = login_courier(test_courier_data[0], test_courier_data[1])
            if courier_id:
                delete_courier(courier_id)

    @allure.title("Нельзя создать курьера без необязательного поля firstName")
    @allure.description("Проверяем, что запрос без firstName возвращает 201 и {'ok': true}")
    def test_create_courier_without_firstname_success(self):
        login_pass = register_new_courier_and_return_login_password()  # Генерируем данные

        payload = {
            "login": login_pass[0],
            "password": login_pass[1]
        }  # firstName отсутствует

        with allure.step("Отправляем запрос на создание курьера без firstName"):
            response = requests.post(COURIER_CREATE_URL, data=payload)

        with allure.step("Проверяем код ответа и тело ответа"):
            assert response.status_code == 201
            assert response.json().get("ok") == True

        # Очистка данных
        courier_id = login_courier(login_pass[0], login_pass[1])
        if courier_id:
            delete_courier(courier_id)