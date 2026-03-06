import os
import redis
import json
import re
from flask import Flask, request, jsonify
from urllib.parse import urlparse
from datetime import datetime
from functools import wraps

app = Flask(__name__)

# Конфигурация Redis
REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
REDIS_DB = int(os.getenv('REDIS_DB', 0))

# Подключение к Redis
redis_client = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    db=REDIS_DB,
    decode_responses=True
)


def extract_domain(url):
    """
    Извлекает домен из URL
    """
    # Добавляем схему, если её нет
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url

    try:
        parsed = urlparse(url)
        domain = parsed.netloc or parsed.path

        # Убираем порт, если есть
        if ':' in domain:
            domain = domain.split(':')[0]

        # Проверяем, что домен не пустой и содержит точку
        if domain and '.' in domain:
            return domain.lower()
        else:
            return None
    except Exception:
        return None


def validate_urls(urls):
    """
    Валидация списка URL
    """
    if not isinstance(urls, list):
        return False, "links должен быть массивом"

    if len(urls) > 1000:  # Ограничение на количество ссылок
        return False, "Слишком много ссылок (максимум 1000)"

    valid_urls = []
    for url in urls:
        if not isinstance(url, str):
            return False, f"Неверный формат URL: {url}"

        domain = extract_domain(url)
        if domain:
            valid_urls.append(domain)

    return True, valid_urls


def handle_errors(f):
    """
    Декоратор для обработки ошибок
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except redis.RedisError as e:
            return jsonify({"status": f"Ошибка Redis: {str(e)}"}), 500
        except Exception as e:
            return jsonify({"status": f"Внутренняя ошибка сервера: {str(e)}"}), 500

    return decorated_function


@app.route('/visited_links', methods=['POST'])
@handle_errors
def visited_links():
    """
    Ресурс для загрузки посещений
    """
    data = request.get_json()

    if not data:
        return jsonify({"status": "Пустой запрос"}), 400

    links = data.get('links')
    if links is None:
        return jsonify({"status": "Отсутствует поле links"}), 400

    # Валидация URL
    is_valid, result = validate_urls(links)
    if not is_valid:
        return jsonify({"status": result}), 400

    domains = result
    if not domains:
        return jsonify({"status": "Нет валидных доменов"}), 400

    # Текущее время как время посещения
    current_time = int(datetime.now().timestamp())

    # Сохраняем домены в Redis (Sorted Set)
    # Используем текущее время как score для возможности поиска по диапазону
    pipeline = redis_client.pipeline()
    for domain in domains:
        pipeline.zadd('visited_domains', {domain: current_time})
    pipeline.execute()

    return jsonify({"status": "ok"})


@app.route('/visited_domains', methods=['GET'])
@handle_errors
def visited_domains():
    """
    Ресурс для получения статистики по доменам
    """
    from_param = request.args.get('from')
    to_param = request.args.get('to')

    # Валидация параметров
    if not from_param or not to_param:
        return jsonify({"status": "Необходимо указать параметры from и to"}), 400

    try:
        from_time = int(from_param)
        to_time = int(to_param)
    except ValueError:
        return jsonify({"status": "Параметры from и to должны быть числами"}), 400

    if from_time > to_time:
        return jsonify({"status": "Параметр from должен быть меньше или равен to"}), 400

    # Получаем уникальные домены за указанный интервал
    # Используем ZRANGEBYSCORE для получения элементов по диапазону времени
    domains = redis_client.zrangebyscore(
        'visited_domains',
        from_time,
        to_time
    )

    # Убираем дубликаты (хотя Redis Sorted Set уже хранит уникальные значения)
    unique_domains = list(set(domains))

    return jsonify({
        "domains": unique_domains,
        "status": "ok"
    })


@app.route('/health', methods=['GET'])
def health():
    """
    Health check endpoint
    """
    try:
        redis_client.ping()
        return jsonify({"status": "healthy"})
    except redis.RedisError:
        return jsonify({"status": "unhealthy"}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)