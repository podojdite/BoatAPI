import random

boat_names = [
    "Черная жемчужина",
    "Летучий Голандец",
    "Призрачный гонщик",
    "Тачка из NFS: Most Wanted",
    "Рай для интровертов",
    "Молния МакУин",
    "Плотва",
    "Даллаский клуб покупателей"
]

crew_names = [
    ["Безумный Джек", "Ржавый Билл", "Кривой Стас"],
    ["Капитан Крабс", "Мистер Сквидварт", "Спанч Боб"],
    ["Чёрный Ус", "Кровавая Лена", "Шалтай Болтай"],
    ["Канеки", "Итачи", "Аянокоджи"]
]

cries = [
    {"text": "За борт капитана!", "frequency": 8, "volume": 9},
    {"text": "ВАААААААЙ!", "frequency": 10, "volume": 10},
    {"text": "Наш новый дом", "frequency": 7, "volume": 8},
    {"text": "Капитан умер да здравствует капитан!", "frequency": 9, "volume": 9},
    {"text": "Бунт! Бунт! БУУУУУУНТ!", "frequency": 1, "volume": 10}
]

def get_random_boat_data():
    return {
        "name": random.choice(boat_names),
        "crew": random.choice(crew_names),
        "cry": random.choice(cries)
    }