

Простой веб-сервис для учета посещенных ссылок с использованием Redis.

## Требования

- Docker
- Docker Compose
- Python 3.7+ (для локального запуска)

## Быстрый старт

### Запуск с помощью Docker Compose

Клонируйте репозиторий:
```bash
git clone <repository-url>
cd link-tracker

Запустите сервисы:

bash
docker-compose up --build

Сервис будет доступен по адресу: http://localhost:5000

Локальный запуск без Docker
Установите зависимости:

bash
pip install -r requirements.txt
Убедитесь, что Redis запущен локально:

bash
redis-server
Запустите приложение:

bash
python app.py
API Endpoints
POST /visited_links
Загрузка массива посещенных ссылок.

Запрос:

json
{
    "links": [
        "https://ya.ru",
        "https://ya.ru?q=123",
        "funbox.ru",
        "https://stackoverflow.com/questions/11828270"
    ]
}
Ответ:

json
{
    "status": "ok"
}
GET /visited_domains
Получение списка уникальных доменов за указанный интервал времени.

Запрос:

text
GET /visited_domains?from=1545221231&to=1545217638
Ответ:

json
{
    "domains": [
        "ya.ru",
        "funbox.ru",
        "stackoverflow.com"
    ],
    "status": "ok"
}
GET /health
Проверка работоспособности сервиса.

Ответ:

json
{
    "status": "healthy"
}
Тестирование
Запуск тестов:

bash
# Локально
pytest tests/ -v

# В Docker
docker-compose exec web pytest tests/ -v
