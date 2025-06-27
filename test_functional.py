def test_create_boat_valid(client):
    """Создание лодки с валидными данными"""
    data = {
        "name": "Тестовая лодка",
        "crew": ["Тестер", "Тестировщик", "QA"],
        "cry": {"text": "Тестим ребят!", "frequency": 5, "volume": 5},
    }
    response = client.post("/api/boats", json=data)
    assert response.status_code == 201
    assert "id" in response.json
    assert response.json["speed"] == 50  # 5*5*2 (из-за "!")


def test_create_boat_missing_name(client):
    """Попытка создания без обязательного поля"""
    response = client.post("/api/boats", json={"crew": ["Тест"], "cry": {}})
    assert response.status_code == 400
    assert "Необходимо указать" in response.json["error"]
