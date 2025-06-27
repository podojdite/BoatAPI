def test_boat_lifecycle(client):
    """Полный жизненный цикл лодки"""
    # 1. Создание
    create_res = client.post(
        "/api/boats",
        json={
            "name": "Жизненный цикл",
            "crew": ["Тест"],
            "cry": {"text": "Тест", "frequency": 5, "volume": 5},
        },
    )
    boat_id = create_res.json["id"]

    # 2. Изменение клича
    update_res = client.put(
        f"/api/boats/{boat_id}/cry", json={"text": "Новенький!", "volume": 8}
    )
    assert update_res.status_code == 200
    assert update_res.json["speed_change"] > 0

    # 3. Бунт
    mutiny_res = client.post(f"/api/boats/{boat_id}/mutiny")
    assert mutiny_res.status_code == 200
    assert mutiny_res.json["new_data"]["name"] != "Жизненный цикл"
