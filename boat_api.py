from flask import Flask, jsonify, request
from uuid import uuid4
import random
from nautical_data import get_random_boat_data

app = Flask(__name__)

# Хранилище лодок в памяти
boats = {}


class Boat:
    def __init__(self, name, crew, cry_text, cry_frequency, cry_volume):
        self.id = str(uuid4())
        self.name = name
        self.crew = crew
        self.speed = 0  # frequency * volume * (Если есть ! в конце текста cry)
        self.cry = {
            "text": cry_text,
            "frequency": cry_frequency,  # Тайминг (через каждые n минут)
            "volume": cry_volume,  # громкость
        }

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "crew": self.crew,
            "speed": self.speed,
            "cry": self.cry,
        }


# Создание лодки
@app.route("/api/boats", methods=["POST"])
def create_boat():
    data = request.get_json()

    # Проверка обязательных полей
    if not data or "name" not in data or "crew" not in data or "cry" not in data:
        return (
            jsonify(
                {
                    "error": "Необходимо указать название, команду и клич",
                    "required_fields": {
                        "name": "string",
                        "crew": "array[string]",
                        "cry": {
                            "text": "string",
                            "frequency": "number",
                            "volume": "number",
                        },
                    },
                }
            ),
            400,
        )

    # Проверка структуры cry
    cry = data["cry"]
    if not all(key in cry for key in ["text", "frequency", "volume"]):
        return (
            jsonify(
                {
                    "error": "Клич должен содержать text, frequency и volume",
                    "example": {
                        "cry": {"text": "АААААААА!", "frequency": 1, "volume": 1}
                    },
                }
            ),
            400,
        )

    frequency = int(cry["frequency"])
    volume = int(cry["volume"])

    # Создаем лодку
    boat = Boat(
        name=data["name"],
        crew=data["crew"],
        cry_text=cry["text"],
        cry_frequency=frequency,
        cry_volume=volume,
    )

    # Рассчитываем начальную скорость
    has_exclamation = cry["text"].endswith("!")
    base_speed = frequency * volume
    boat.speed = base_speed * (2 if has_exclamation else 1)

    boats[boat.id] = boat

    return (
        jsonify(
            {
                **boat.to_dict(),
                "message": f"Лодка создана с начальной скоростью {boat.speed}",
                "speed_calculation": {
                    "base": base_speed,
                    "bonus": "2x (восклицательный клич)" if has_exclamation else "нет",
                },
            }
        ),
        201,
    )


# Получение состояния лодки
@app.route("/api/boats/<boat_id>", methods=["GET"])
def get_boat_status(boat_id):
    boat = boats.get(boat_id)

    if not boat:
        return jsonify({"error": "Лодка не найдена"}), 404

    return jsonify(boat.to_dict())


# Изменение клича
@app.route("/api/boats/<boat_id>/cry", methods=["PUT"])
def update_cry(boat_id):
    boat = boats.get(boat_id)

    if not boat:
        return jsonify({"error": "Лодка не найдена"}), 404

    data = request.get_json()

    # Получаем новые параметры (если переданы)
    new_text = data.get("text")
    new_frequency = data.get("frequency")
    new_volume = data.get("volume")

    # Рассчитываем изменение скорости
    speed_change, has_exclamation = calculate_speed_change(
        boat, new_frequency=new_frequency, new_volume=new_volume, new_text=new_text
    )

    # Обновляем параметры
    if new_text is not None:
        boat.cry["text"] = new_text
    if new_frequency is not None:
        boat.cry["frequency"] = new_frequency
    if new_volume is not None:
        boat.cry["volume"] = new_volume

    # Применяем изменение скорости
    boat.speed = max(0, boat.speed + speed_change)

    return jsonify(
        {
            "message": f"Клич лодки '{boat.name}' обновлен!",
            "updated_cry": boat.cry,
            "speed_change": speed_change,
            "new_speed": boat.speed,
            "effect": "Удвоенный эффект!" if has_exclamation else "Обычный эффект",
        }
    )


# Бунт на лодке
@app.route("/api/boats/<boat_id>/mutiny", methods=["POST"])
def mutiny(boat_id):
    boat = boats.get(boat_id)

    if not boat:
        return jsonify({"error": "Лодка не найдена"}), 404

    # Сохраняем старые значения для отчета
    old_data = boat.to_dict()

    # Получаем случайные новые данные
    new_data = get_random_boat_data()

    # Рассчитываем изменение скорости от новых параметров
    speed_change, has_exclamation = calculate_speed_change(
        boat,
        new_frequency=new_data["cry"]["frequency"],
        new_volume=new_data["cry"]["volume"],
        new_text=new_data["cry"]["text"],
    )

    # Обновляем лодку
    boat.name = new_data["name"]
    boat.crew = new_data["crew"]
    boat.cry = new_data["cry"]

    return jsonify(
        {
            "message": f"На '{old_data['name']}' произошел бунт!",
            "old_data": old_data,
            "new_data": boat.to_dict(),
            "speed_change": speed_change,
            "effect": "Удвоенный эффект!" if has_exclamation else "Обычный эффект",
            "warning": "Внимание! Все параметры лодки изменены!",
        }
    )


def calculate_speed_change(boat, new_frequency=None, new_volume=None, new_text=None):
    """
    Рассчитывает изменение скорости на основе новых параметров клича
    Возвращает изменение скорости и флаг восклицания
    """
    old_frequency = boat.cry["frequency"]
    old_volume = boat.cry["volume"]

    # Используем новые значения или текущие, если не переданы
    freq = new_frequency if new_frequency is not None else old_frequency
    vol = new_volume if new_volume is not None else old_volume
    text = new_text if new_text is not None else boat.cry["text"]

    # Проверяем есть ли "!" в тексте
    has_exclamation = text.endswith("!")

    # Рассчитываем изменение скорости
    speed_change = (freq * vol) - (old_frequency * old_volume)

    # Если есть восклицательный знак - удваиваем эффект
    if has_exclamation:
        speed_change *= 2

    return speed_change, has_exclamation


if __name__ == "__main__":
    app.run(debug=True)
