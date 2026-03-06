import asyncio
import sys
import os

# Добавляем текущую директорию в путь для импорта
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Теперь импортируем нашу библиотеку
try:
    from matrix_processor import get_matrix, HAS_AIOHTTP

    print(f"Библиотека успешно импортирована")
    print(f"Используется: {'aiohttp' if HAS_AIOHTTP else 'стандартная библиотека'}")
except ImportError as e:
    print(f"Ошибка импорта: {e}")
    print("Убедитесь, что файл matrix_processor.py находится в той же директории")
    sys.exit(1)


async def test_from_condition() -> None:
    """Тест из условия задачи"""
    print("\n" + "=" * 50)
    print("Тест из условия задачи")
    print("=" * 50)

    # Создаем тестовый файл с матрицей из условия
    test_matrix_content = """+-----+-----+-----+-----+
|  10 |  20 |  30 |  40 |
+-----+-----+-----+-----+
|  50 |  60 |  70 |  80 |
+-----+-----+-----+-----+
|  90 | 100 | 110 | 120 |
+-----+-----+-----+-----+
| 130 | 140 | 150 | 160 |
+-----+-----+-----+-----+"""

    # Сохраняем в файл
    with open('test_matrix.txt', 'w', encoding='utf-8') as f:
        f.write(test_matrix_content)

    try:
        # Ожидаемый результат из условия
        EXPECTED = [
            10, 50, 90, 130,
            140, 150, 160, 120,
            80, 40, 30, 20,
            60, 100, 110, 70,
        ]

        # Получаем абсолютный путь к файлу
        current_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_dir, 'test_matrix.txt')
        file_url = f"file://{file_path}"

        print(f"\nТестируем с файлом: {file_path}")

        # Вызываем нашу функцию
        result = await get_matrix(file_url)

        # Проверяем результат
        print(f"\nРезультат получен!")
        print(f"Количество элементов: {len(result)}")

        if result == EXPECTED:
            print("Тест ПРОЙДЕН! Результат совпадает с ожидаемым!")
        else:
            print("Тест НЕ ПРОЙДЕН!")
            print(f"\nОжидалось: {EXPECTED}")
            print(f"\nПолучено:  {result}")

            # Найдем различия
            differences = []
            for i, (exp, got) in enumerate(zip(EXPECTED, result)):
                if exp != got:
                    differences.append(f"Позиция {i}: ожидалось {exp}, получено {got}")

            if differences:
                print("\nРазличия:")
                for diff in differences:
                    print(f"  - {diff}")

        # Выведем результат в красивом формате
        print(f"\nРезультат обхода:")
        for i in range(0, len(result), 4):
            print(f"  {result[i:i + 4]}")

    except Exception as e:
        print(f"\nОшибка: {type(e).__name__}: {e}")

    finally:
        # Удаляем временный файл
        if os.path.exists('test_matrix.txt'):
            os.remove('test_matrix.txt')


async def test_3x3_matrix() -> None:
    """Тест с матрицей 3x3"""
    print("\n" + "=" * 50)
    print("Тест с матрицей 3x3")
    print("=" * 50)

    test_matrix_content = """+-----+-----+-----+
|   1 |   2 |   3 |
+-----+-----+-----+
|   4 |   5 |   6 |
+-----+-----+-----+
|   7 |   8 |   9 |
+-----+-----+-----+"""

    with open('test_3x3.txt', 'w', encoding='utf-8') as f:
        f.write(test_matrix_content)

    try:
        # Ожидаемый результат для 3x3
        EXPECTED = [1, 4, 7, 8, 9, 6, 3, 2, 5]

        file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test_3x3.txt')
        file_url = f"file://{file_path}"

        result = await get_matrix(file_url)

        print(f"\nМатрица 3x3:")
        print("  1 2 3")
        print("  4 5 6")
        print("  7 8 9")

        print(f"\nРезультат обхода: {result}")

        if result == EXPECTED:
            print("Тест 3x3 ПРОЙДЕН!")
        else:
            print("Тест 3x3 НЕ ПРОЙДЕН!")
            print(f"Ожидалось: {EXPECTED}")

    except Exception as e:
        print(f"Ошибка: {e}")

    finally:
        if os.path.exists('test_3x3.txt'):
            os.remove('test_3x3.txt')


async def test_from_url() -> None:
    """Попытка загрузить с реального URL"""
    print("\n" + "=" * 50)
    print("Тест загрузки с HTTP URL")
    print("=" * 50)

    # Пример URL с тестовой матрицей (может не работать без интернета)
    test_url = "https://raw.githubusercontent.com/avito-tech/python-trainee-assignment/main/matrix.txt"

    print(f"\nПопытка загрузки с: {test_url}")
    print("(Если нет интернета, этот тест пропустится)")

    try:
        result = await get_matrix(test_url)
        print(f"\nУспешно загружено с URL!")
        print(f"Получено элементов: {len(result)}")

        # Проверяем, соответствует ли результат ожидаемому
        EXPECTED = [
            10, 50, 90, 130,
            140, 150, 160, 120,
            80, 40, 30, 20,
            60, 100, 110, 70,
        ]

        if result == EXPECTED:
            print("✅ Результат совпадает с ожидаемым!")
        else:
            print("⚠️ Результат не совпадает с ожидаемым")
            print(f"Первые 8 элементов: {result[:8]}")

    except Exception as e:
        print(f"ℹ️ Не удалось загрузить с URL: {type(e).__name__}: {e}")
        print("Это нормально, если нет интернета или URL недоступен.")


async def main():
    """Основная функция"""
    print("🚀 Запуск тестов библиотеки matrix_processor")
    print("-" * 50)

    # Запускаем все тесты
    await test_from_condition()
    await test_3x3_matrix()
    await test_from_url()

    print("\n" + "=" * 50)
    print("Все тесты завершены!")
    print("=" * 50)


if __name__ == "__main__":
    # Проверяем Python версию
    if sys.version_info < (3, 7):
        print("❌ Требуется Python 3.7 или выше")
        sys.exit(1)

    # Запускаем асинхронную основную функцию
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n👋 Программа прервана пользователем")
    except Exception as e:
        print(f"\n❌ Неожиданная ошибка: {e}")
        import traceback

        traceback.print_exc()