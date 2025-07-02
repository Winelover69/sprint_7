import pytest
import requests
from courier_generator import register_new_courier_and_return_login_password, login_courier, delete_courier
from urls import COURIER_LOGIN_URL, COURIER_CREATE_URL, COURIER_DELETE_URL

@pytest.fixture(scope="function")
def new_courier_data():

    login_pass_name = register_new_courier_and_return_login_password()
    if not login_pass_name:
        pytest.fail("Не удалось создать курьера для теста.")

    login, password, first_name = login_pass_name[0], login_pass_name[1], login_pass_name[2]
    courier_id = login_courier(login, password)

    yield {
        "login": login,
        "password": password,
        "firstName": first_name,
        "id": courier_id # ID может быть None, если логин не удался
    }

    if courier_id:
        delete_courier(courier_id)