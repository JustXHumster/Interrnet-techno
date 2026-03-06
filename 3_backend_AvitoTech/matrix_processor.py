import asyncio
import logging
from typing import List
import sys
import os

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MatrixProcessingError(Exception):
    """Базовое исключение для ошибок обработки матрицы"""
    pass


class NetworkError(MatrixProcessingError):
    """Ошибка сетевого взаимодействия"""
    pass


class InvalidMatrixError(MatrixProcessingError):
    """Некорректный формат матрицы"""
    pass


def parse_matrix_from_text(text: str) -> List[List[int]]:
    """
    Парсит матрицу из текста.
    Ожидает формат с разделителями '|' и '-'
    """
    lines = text.strip().split('\n')
    matrix = []

    for line in lines:
        # Пропускаем строки с границами таблицы
        if line.startswith('+') or not line.strip():
            continue

        # Разделяем строку по символу '|' и фильтруем
        parts = []
        for part in line.split('|'):
            stripped = part.strip()
            if stripped and not stripped.startswith('-'):
                parts.append(stripped)

        # Преобразуем в числа
        try:
            row = [int(num) for num in parts]
            matrix.append(row)
        except ValueError as e:
            raise InvalidMatrixError(f"Не удалось преобразовать значение в число: {e}")

    # Проверяем, что матрица не пустая
    if not matrix:
        raise InvalidMatrixError("Матрица пуста")

    # Проверяем, что матрица квадратная
    n = len(matrix)
    for i, row in enumerate(matrix):
        if len(row) != n:
            raise InvalidMatrixError(
                f"Строка {i} имеет длину {len(row)}, ожидалось {n}. "
                "Матрица должна быть квадратной."
            )

    return matrix


def traverse_matrix_counter_clockwise(matrix: List[List[int]]) -> List[int]:
    """
    Обходит матрицу по спирали против часовой стрелки,
    начиная с левого верхнего угла.
    """
    if not matrix:
        return []

    n = len(matrix)
    result = []

    # Границы для обхода
    top = 0
    bottom = n - 1
    left = 0
    right = n - 1

    while top <= bottom and left <= right:
        # Спускаемся вниз по левой колонке
        for i in range(top, bottom + 1):
            result.append(matrix[i][left])
        left += 1

        # Идём вправо по нижней строке
        for i in range(left, right + 1):
            result.append(matrix[bottom][i])
        bottom -= 1

        # Проверяем, остались ли строки/столбцы для обхода
        if left <= right:
            # Поднимаемся вверх по правой колонке
            for i in range(bottom, top - 1, -1):
                result.append(matrix[i][right])
            right -= 1

        if top <= bottom:
            # Идём влево по верхней строке
            for i in range(right, left - 1, -1):
                result.append(matrix[top][i])
            top += 1

    return result


# Попробуем импортировать aiohttp
try:
    import aiohttp
    from aiohttp import ClientSession, ClientTimeout, ClientError

    HAS_AIOHTTP = True


    async def fetch_url_async(url: str) -> str:
        """Асинхронная загрузка URL с использованием aiohttp"""
        # Проверяем, не file:// ли это URL
        if url.startswith('file://'):
            # Для file:// протокола читаем файл напрямую
            file_path = url[7:]  # Убираем 'file://'
            # На Windows путь может начинаться с /, убираем его
            if file_path.startswith('/') and os.name == 'nt':
                file_path = file_path[1:]

            loop = asyncio.get_event_loop()

            def read_file():
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        return f.read()
                except FileNotFoundError:
                    raise NetworkError(f"Файл не найден: {file_path}")
                except Exception as e:
                    raise NetworkError(f"Ошибка чтения файла: {str(e)}")

            return await loop.run_in_executor(None, read_file)

        # Для HTTP/HTTPS используем aiohttp
        timeout = ClientTimeout(total=10)

        try:
            async with ClientSession(timeout=timeout) as session:
                async with session.get(url) as response:
                    if response.status >= 400:
                        raise NetworkError(f"HTTP ошибка: {response.status}")
                    return await response.text()
        except asyncio.TimeoutError:
            raise NetworkError("Таймаут при подключении к серверу")
        except ClientError as e:
            raise NetworkError(f"Ошибка сети: {str(e)}")
        except Exception as e:
            raise NetworkError(f"Неожиданная ошибка: {str(e)}")

except ImportError:
    HAS_AIOHTTP = False


    # Fallback на синхронные запросы
    async def fetch_url_async(url: str) -> str:
        """Синхронная загрузка URL (fallback если aiohttp недоступен)"""
        import urllib.request
        import urllib.error

        try:
            # Используем синхронный запрос в отдельном потоке
            loop = asyncio.get_event_loop()

            def fetch():
                # Для file:// протокола используем прямое чтение файла
                if url.startswith('file://'):
                    file_path = url[7:]  # Убираем 'file://'
                    # На Windows путь может начинаться с /, убираем его
                    if file_path.startswith('/') and os.name == 'nt':
                        file_path = file_path[1:]

                    with open(file_path, 'r', encoding='utf-8') as f:
                        return f.read()

                # Для HTTP/HTTPS используем urllib
                request = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(request, timeout=10) as response:
                    if response.status >= 400:
                        raise NetworkError(f"HTTP ошибка: {response.status}")
                    return response.read().decode('utf-8')

            return await loop.run_in_executor(None, fetch)
        except FileNotFoundError as e:
            raise NetworkError(f"Файл не найден: {e}")
        except urllib.error.URLError as e:
            raise NetworkError(f"Ошибка URL: {str(e)}")
        except TimeoutError:
            raise NetworkError("Таймаут при подключении к серверу")
        except Exception as e:
            if isinstance(e, NetworkError):
                raise
            raise NetworkError(f"Ошибка загрузки: {str(e)}")


async def get_matrix(url: str) -> List[int]:
    """
    Асинхронно загружает матрицу с сервера и возвращает результат
    обхода по спирали против часовой стрелки.
    """
    try:
        logger.info(f"Загрузка матрицы с URL: {url}")

        # Загружаем данные с URL
        text = await fetch_url_async(url)

        if not text:
            raise InvalidMatrixError("Получен пустой ответ от сервера")

        # Парсим матрицу из текста
        try:
            matrix = parse_matrix_from_text(text)
            logger.info(f"Успешно распарсена матрица {len(matrix)}x{len(matrix)}")
        except InvalidMatrixError:
            raise
        except Exception as e:
            raise InvalidMatrixError(f"Ошибка при парсинге матрицы: {str(e)}")

        # Выполняем обход матрицы
        result = traverse_matrix_counter_clockwise(matrix)

        logger.info(f"Успешно обработана матрица, результат содержит {len(result)} элементов")
        return result

    except (NetworkError, InvalidMatrixError):
        raise
    except Exception as e:
        logger.error(f"Неожиданная ошибка: {str(e)}")
        raise MatrixProcessingError(f"Не удалось обработать матрицу: {str(e)}")


# Простая функция для тестирования без сервера
async def get_matrix_from_text(text: str) -> List[int]:
    """
    Вспомогательная функция для тестирования с текстом матрицы
    """
    matrix = parse_matrix_from_text(text)
    return traverse_matrix_counter_clockwise(matrix)