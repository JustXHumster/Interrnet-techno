# game_scores.py
from pprint import pprint
import random
import math

TIMESTAMPS_COUNT = 50000

PROBABILITY_SCORE_CHANGED = 0.0001

PROBABILITY_HOME_SCORE = 0.45

OFFSET_MAX_STEP = 3

INITIAL_STAMP = {
    "offset": 0,
    "score": {
        "home": 0,
        "away": 0
    }
}


def generate_stamp(previous_value):
    score_changed = random.random() > 1 - PROBABILITY_SCORE_CHANGED
    home_score_change = 1 if score_changed and random.random() > 1 - \
                             PROBABILITY_HOME_SCORE else 0
    away_score_change = 1 if score_changed and not home_score_change else 0
    offset_change = math.floor(random.random() * OFFSET_MAX_STEP) + 1

    return {
        "offset": previous_value["offset"] + offset_change,
        "score": {
            "home": previous_value["score"]["home"] + home_score_change,
            "away": previous_value["score"]["away"] + away_score_change
        }
    }


def generate_game():
    stamps = [INITIAL_STAMP, ]
    current_stamp = INITIAL_STAMP
    for _ in range(TIMESTAMPS_COUNT):
        current_stamp = generate_stamp(current_stamp)
        stamps.append(current_stamp)

    return stamps


def get_score(game_stamps, offset):
    '''
    Takes list of game's stamps and time offset for which returns the scores for the home and away teams.
    Please pay attention to that for some offsets the game_stamps list may not contain scores.
    '''
    if not game_stamps:
        return 0, 0

    # Если offset меньше первого timestamp, возвращаем начальный счет
    if offset < game_stamps[0]["offset"]:
        return game_stamps[0]["score"]["home"], game_stamps[0]["score"]["away"]

    # Если offset больше последнего timestamp, возвращаем конечный счет
    if offset >= game_stamps[-1]["offset"]:
        return game_stamps[-1]["score"]["home"], game_stamps[-1]["score"]["away"]

    # Бинарный поиск последнего stamp с offset <= заданному
    left, right = 0, len(game_stamps) - 1

    while left <= right:
        mid = (left + right) // 2
        current_offset = game_stamps[mid]["offset"]

        if current_offset == offset:
            # Нашли точное совпадение
            return game_stamps[mid]["score"]["home"], game_stamps[mid]["score"]["away"]
        elif current_offset < offset:
            left = mid + 1
        else:
            right = mid - 1

    # После завершения цикла:
    # - left указывает на первый элемент с offset > заданного
    # - right указывает на последний элемент с offset <= заданного (наш искомый)
    # Цикл гарантированно завершится с right >= 0, так как мы обработали edge cases выше

    return game_stamps[right]["score"]["home"], game_stamps[right]["score"]["away"]


# Генерация данных
game_stamps = generate_game()

# Демонстрация работы функции
if __name__ == "__main__":
    # Тестирование функции
    print("Примеры работы функции get_score:")
    print("-" * 40)

    # Пример 1: Начало игры
    print(f"1. offset = 0: {get_score(game_stamps, 0)}")

    # Пример 2: Случайный offset в середине
    middle_index = len(game_stamps) // 2
    random_offset = game_stamps[middle_index]["offset"]
    print(f"2. offset = {random_offset} (существует в stamps): {get_score(game_stamps, random_offset)}")

    # Пример 3: offset между двумя stamps
    # Найдем два соседних stamps
    for i in range(1, len(game_stamps)):
        if game_stamps[i]["offset"] - game_stamps[i - 1]["offset"] > 1:
            between_offset = game_stamps[i - 1]["offset"] + 1
            prev_score = get_score(game_stamps, game_stamps[i - 1]["offset"])
            between_score = get_score(game_stamps, between_offset)
            print(
                f"3. offset = {between_offset} (между stamps): {between_score} (должен совпадать с offset={game_stamps[i - 1]['offset']}: {prev_score})")
            break

    # Пример 4: offset меньше минимального
    print(f"4. offset = -5 (меньше минимального): {get_score(game_stamps, -5)}")

    # Пример 5: offset больше максимального
    max_offset = game_stamps[-1]["offset"]
    print(f"5. offset = {max_offset + 10} (больше максимального): {get_score(game_stamps, max_offset + 10)}")

    print("\n" + "=" * 40)
    print("Первые 10 stamps для проверки:")
    print("-" * 40)
    for i in range(min(10, len(game_stamps))):
        stamp = game_stamps[i]
        print(f"offset: {stamp['offset']:3d}, score: {stamp['score']['home']}:{stamp['score']['away']}")