import pytest
import requests
import allure
from urls import COURIER_CREATE_URL
# Импортируем только необходимые функции из courier_generator
from courier_generator import generate_random_string, login_courier, \
    delete_courier  # <-- Изменено: импортируем generate_random_string напрямую


@allure.suite("API тесты: Создание курьера")
class TestCreateCourier:

    # Используем фикстуру new_courier_data для гарантированной очистки
    @allure.title("Успешное создание курьера: проверка ID через фикстуру")
    @allure.description("Проверяем, что фикстура успешно создает курьера и возвращает его ID")
    def test_courier_id_is_returned_by_fixture(self, new_courier_data):
        # Этот тест просто подтверждает, что фикстура new_courier_data
        # успешно создала курьера и предоставила его ID.
        # Проверка статуса 201 и {"ok":true} уже неявно гарантируется фикстурой
        # и/или может быть явно проверена в test_create_courier_returns_201_ok_true,
        # который сам инициирует создание.
        with allure.step("Проверяем, что ID курьера был успешно получен"):
            assert new_courier_data["id"] is not None
            allure.attach(f"ID созданного курьера: {new_courier_data['id']}", name="Курьер ID",
                          attachment_type=allure.attachment_type.TEXT)

    @allure.title("Успешное создание курьера: статус 201 и 'ok':true")
    @allure.description("Проверяем, что курьера можно создать, и запрос возвращает 201 и {'ok': true}")
    def test_create_courier_returns_201_ok_true(self):
        login = generate_random_string(10)
        password = generate_random_string(10)
        first_name = generate_random_string(10)

        payload = {
            "login": login,
            "password": password,
            "firstName": first_name
        }
        courier_id = None  # Инициализируем для очистки

        try:
            with allure.step("Отправляем запрос на создание курьера"):
                response = requests.post(COURIER_CREATE_URL, data=payload)

            with allure.step("Проверяем код ответа и тело ответа"):
                assert response.status_code == 201
                assert response.json().get("ok") == True

            # Получаем ID курьера для последующего удаления
            courier_id = login_courier(login, password)
            assert courier_id is not None, "Не удалось получить ID созданного курьера для очистки."

        finally:
            # Очистка данных после теста
            if courier_id:
                with allure.step(f"Очистка: удаление курьера с ID: {courier_id}"):
                    delete_courier(courier_id)
            else:
                allure.attach(f"Курьер '{login}' не был создан или не удалось получить его ID, очистка пропущена.",
                              name="Очистка пропущена", attachment_type=allure.attachment_type.TEXT)

    @allure.title("Невозможно создать двух одинаковых курьеров")
    @allure.description("Проверяем, что при попытке создать курьера с существующим логином возвращается ошибка 409")
    def test_create_duplicate_courier_fails(self, new_courier_data):
        payload = {
            "login": new_courier_data["login"],  # Используем логин уже созданного курьера
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
    def test_create_courier_without_required_field_fails(self, missing_field):
        # Генерируем уникальные данные для попытки создания
        login = generate_random_string(10)
        password = generate_random_string(10)
        first_name = generate_random_string(10)

        payload = {
            "login": login,
            "password": password,
            "firstName": first_name
        }
        payload.pop(missing_field)  # Удаляем одно из обязательных полей

        with allure.step(f"Отправляем запрос на создание курьера без поля '{missing_field}'"):
            response = requests.post(COURIER_CREATE_URL, data=payload)

        with allure.step("Проверяем код ответа и тело ответа"):
            assert response.status_code == 400
            assert response.json().get("message") == "Недостаточно данных для создания учетной записи"

        # Здесь нет необходимости в блоке if/else или очистке,
        # так как тест ожидает ошибку 400 и курьер не должен быть создан.
        # Если бы вдруг вернулся 201, тест бы упал на assert response.status_code == 400.

    @allure.title("Нельзя создать курьера без необязательного поля firstName")
    @allure.description("Проверяем, что запрос без firstName возвращает 201 и {'ok': true}")
    def test_create_courier_without_firstname_success(self):
        login = generate_random_string(10)
        password = generate_random_string(10)

        payload = {
            "login": login,
            "password": password
        }  # firstName отсутствует
        courier_id = None  # Инициализируем для очистки

        try:
            with allure.step("Отправляем запрос на создание курьера без firstName"):
                response = requests.post(COURIER_CREATE_URL, data=payload)

            with allure.step("Проверяем код ответа и тело ответа"):
                assert response.status_code == 201
                assert response.json().get("ok") == True

            # Получаем ID курьера для последующего удаления
            courier_id = login_courier(login, password)
            assert courier_id is not None, "Не удалось получить ID созданного курьера для очистки."

        finally:
            # Очистка данных после теста
            if courier_id:
                with allure.step(f"Очистка: удаление курьера с ID: {courier_id}"):
                    delete_courier(courier_id)
            else:
                allure.attach(f"Курьер '{login}' не был создан или не удалось получить его ID, очистка пропущена.",
                              name="Очистка пропущена", attachment_type=allure.attachment_type.TEXT)

    @allure.title("Ошибка при создании курьера с уже существующим логином")
    @allure.description("Проверяем, что если логин уже используется, возвращается ошибка 409")
    def test_create_courier_with_existing_login_fails(self, new_courier_data):
        # new_courier_data уже создает и удаляет курьера, мы используем его логин для дублирования
        existing_login = new_courier_data["login"]

        payload = {
            "login": existing_login,
            "password": generate_random_string(10),
            "firstName": generate_random_string(10)
        }
        with allure.step(f"Отправляем запрос на создание курьера с уже существующим логином '{existing_login}'"):
            response = requests.post(COURIER_CREATE_URL, data=payload)

        with allure.step("Проверяем код ответа и тело ответа"):
            assert response.status_code == 409
            assert response.json().get("message") == "Этот логин уже используется. Попробуйте другой.")