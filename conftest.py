import pytest
import requests
import allure
from courier_generator import generate_random_string, register_new_courier, login_courier, delete_courier
from urls import COURIER_CREATE_URL, COURIER_LOGIN_URL, COURIER_DELETE_URL


@pytest.fixture(scope="function")
def unique_courier_credentials():
    """
    Фикстура для генерации уникальных учетных данных курьера.
    Не отправляет запросы к API.
    Возвращает словарь {"login": ..., "password": ..., "firstName": ...}.
    """
    login = generate_random_string(10)
    password = generate_random_string(10)
    first_name = generate_random_string(10)

    with allure.step("Генерация уникальных учетных данных курьера"):
        allure.attach(f"Login: {login}, Password: {password}, FirstName: {first_name}", name="Сгенерированные данные",
                      attachment_type=allure.attachment_type.TEXT)

    return {
        "login": login,
        "password": password,
        "firstName": first_name
    }


@pytest.fixture(scope="function")
def created_courier_and_cleanup():
    """
    Фикстура для создания курьера перед тестом и его удаления после.
    Возвращает словарь с данными курьера и его ID.
    Если курьер не создается или не логинится, фикстура проваливается.
    """
    courier_login = generate_random_string(10)
    courier_password = generate_random_string(10)
    courier_first_name = generate_random_string(10)
    courier_id = None

    payload = {
        "login": courier_login,
        "password": courier_password,
        "firstName": courier_first_name
    }

    try:
        with allure.step(f"Подготовка: создание тестового курьера с логином '{courier_login}'"):
            response = requests.post(COURIER_CREATE_URL, data=payload)
            # Проверяем успешность создания прямо в фикстуре, так как это необходимо для ее работы
            assert response.status_code == 201, f"Фикстура: Ошибка создания курьера (статус {response.status_code}): {response.text}"
            assert response.json().get(
                "ok") is True, f"Фикстура: Ошибка создания курьера (тело ответа): {response.text}"

        with allure.step(f"Подготовка: логин курьера '{courier_login}' для получения ID"):
            courier_id = login_courier(courier_login, courier_password)
            assert courier_id is not None, f"Фикстура: Не удалось залогиниться под созданным курьером '{courier_login}' для получения ID."

        yield {
            "login": courier_login,
            "password": courier_password,
            "firstName": courier_first_name,
            "id": courier_id
        }

    finally:
        # Удаляем курьера после теста, независимо от исхода
        if courier_id:
            with allure.step(f"Очистка: удаление тестового курьера с ID: {courier_id}"):
                if not delete_courier(courier_id):
                    allure.attach(f"Не удалось удалить курьера с ID: {courier_id}", name="Ошибка очистки",
                                  attachment_type=allure.attachment_type.TEXT)
                    # Можно добавить pytest.fail("Ошибка очистки: не удалось удалить тестового курьера.") если это критично.
                else:
                    allure.attach(f"Курьер с ID: {courier_id} успешно удален.", name="Очистка",
                                  attachment_type=allure.attachment_type.TEXT)
        else:
            allure.attach("Очистка: ID курьера для удаления не был получен, удаление пропущено.",
                          name="Очистка пропущена", attachment_type=allure.attachment_type.TEXT)