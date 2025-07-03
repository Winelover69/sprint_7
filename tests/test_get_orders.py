import pytest
import requests
import allure
from urls import ORDER_LIST_URL


@allure.suite("API тесты: Список заказов")
class TestGetOrdersList:

    @allure.title("Получение списка заказов")
    @allure.description("Проверяем, что запрос возвращает список заказов в теле ответа")
    def test_get_orders_list_success(self):
        with allure.step("Отправляем запрос на получение списка заказов"):
            response = requests.get(ORDER_LIST_URL)

        with allure.step("Проверяем код ответа и структуру тела ответа"):
            assert response.status_code == 200
            assert "orders" in response.json()  # Проверяем наличие ключа 'orders'
            assert isinstance(response.json()["orders"], list)  # Проверяем, что 'orders' является списком
            # Можно также проверить, что список не пустой, если ожидается наличие заказов
            # assert len(response.json()["orders"]) > 0