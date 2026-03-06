Описание
Программа генерирует последовательность временных меток (stamps), каждая из которых содержит:

offset - временная метка (в условных единицах)

score - текущий счет матча (домашняя и гостевая команды)

Затем предоставляется функция get_score(game_stamps, offset) для получения счета на любой момент времени.

Особенности генерации данных
TIMESTAMPS_COUNT = 50000 - генерируется 50,000 временных меток

PROBABILITY_SCORE_CHANGED = 0.0001 - низкая вероятность изменения счета на каждом шаге

OFFSET_MAX_STEP = 3 - временные метки увеличиваются на 1-3 единицы за шаг

PROBABILITY_HOME_SCORE = 0.45 - если счет меняется, с вероятностью 45% забивает домашняя команда

#Локальный запуск

git clone <repository-url>
cd game-score-tracker


python game_scores.py

№Запуск через Docker

docker build -t game-scores .

docker run --rm game-scores