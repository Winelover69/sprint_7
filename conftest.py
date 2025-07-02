import pytest
import requests
import allure
from courier_generator import register_new_courier_and_return_login_password, login_courier, delete_courier, BASE_URL
from urls import COURIER_LOGIN_URL, COURIER_CREATE_URL, COURIER_DELETE_URL


@pytest.fixture(scope="function")
def new_courier_data():
    """
    Фикстура для создания нового курьера перед тестом
    и его удаления после теста. Возвращает [login, password, firstName, courier_id].
    """
    with allure.step("Подготовка тестового курьера: создание"):
        login, password, first_name = register_new_courier_and_return_login_password()  # Возвращает None, если регистрация не 201

        if not login:  # Если register_new_courier_and_return_login_password вернул пустой список
            pytest.fail("Не удалось создать курьера для фикстуры. Проверьте метод регистрации.")

        with allure.step(f"Логинимся курьером '{login}' для получения ID"):
            courier_id = login_courier(login, password)
            if courier_id is None:
                pytest.fail(f"Не удалось залогиниться под созданным курьером '{login}' для получения ID.")

        yield {
            "login": login,
            "password": password,
            "firstName": first_name,
            "id": courier_id
        }

    with allure.step(f"Очистка: удаление тестового курьера с ID: {courier_id}"):
        if courier_id:  # Убедимся, что ID курьера существует перед попыткой удаления
            if not delete_courier(courier_id):
                allure.attach(f"Не удалось удалить курьера с ID: {courier_id}", name="Ошибка очистки",
                              attachment_type=allure.attachment_type.TEXT)
                # pytest.fail("Ошибка очистки: не удалось удалить тестового курьера.") # Можно провалить, если очистка критична
            else:
                allure.attach(f"Курьер с ID: {courier_id} успешно удален.", name="Очистка",
                              attachment_type=allure.attachment_type.TEXT)rier_id)