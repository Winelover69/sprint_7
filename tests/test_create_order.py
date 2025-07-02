import pytest
import requests
import allure
from urls import ORDER_CREATE_URL

@allure.suite("API тесты: Создание заказа")
class TestCreateOrder:

    # Используем параметризацию для разных цветов и комбинаций
    @allure.title("Успешное создание заказа с разными вариантами цвета")
    @allure.description("Проверяем, что заказ можно создать с указанием одного цвета, обоих цветов или без цвета")
    @pytest.mark.parametrize("color", [
        ["BLACK"],             # Один цвет
        ["GREY"],              # Другой цвет
        ["BLACK", "GREY"],     # Оба цвета
        []                     # Без цвета
    ])
    def test_create_order_with_color_options_success(self, color):
        payload = {
            "firstName": "Naruto",
            "lastName": "Uchiha",
            "address": "Konoha, 142 apt",
            "metroStation": 4,
            "phone": "+7 800 355 35 35",
            "rentTime": 5,
            "deliveryDate": "2024-12-31",
            "comment": "Saske, come back to Konoha",
            "color": color
        }
        with allure.step(f"Отправляем запрос на создание заказа с цветом(ами): {color}"):
            response = requests.post(ORDER_CREATE_URL, json=payload) # Важно: для такого тела запроса используем json=payload

        with allure.step("Проверяем код ответа и тело ответа"):
            assert response.status_code == 201
            assert "track" in response.json()
            assert response.json()["track"] is not None

        # В идеале, после создания заказа, его нужно удалить,
        # но для этого нужен отдельный эндпоинт "отмена заказа",
        # который будет протестирован в дополнительном задании.
        # Пока оставляем заказы в системе.