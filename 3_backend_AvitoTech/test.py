import asyncio
import sys
import os

# Добавляем текущую директорию в путь
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from matrix_processor import get_matrix


async def test_get_matrix():
    """Точный тест из условия задачи"""
    # Создаем файл matrix.txt как в условии
    matrix_content = """+-----+-----+-----+-----+
|  10 |  20 |  30 |  40 |
+-----+-----+-----+-----+
|  50 |  60 |  70 |  80 |
+-----+-----+-----+-----+
|  90 | 100 | 110 | 120 |
+-----+-----+-----+-----+
| 130 | 140 | 150 | 160 |
+-----+-----+-----+-----+"""

    # Сохраняем в файл
    with open('matrix.txt', 'w', encoding='utf-8') as f:
        f.write(matrix_content)

    try:
        # Ожидаемый результат из условия
        TRAVERSAL = [
            10, 50, 90, 130,
            140, 150, 160, 120,
            80, 40, 30, 20,
            60, 100, 110, 70,
        ]

        # Используем file:// протокол
        file_path = os.path.abspath('matrix.txt')
        result = await get_matrix(f"file://{file_path}")

        # Проверяем результат
        assert result == TRAVERSAL, f"Ожидалось {TRAVERSAL}, получено {result}"
        print("✅ Тест пройден успешно!")
        return True

    finally:
        # Удаляем временный файл
        if os.path.exists('matrix.txt'):
            os.remove('matrix.txt')


if __name__ == "__main__":
    print("Запуск теста из условия задачи...")
    try:
        success = asyncio.run(test_get_matrix())
        if success:
            print("🎉 Все тесты пройдены!")
            sys.exit(0)
        else:
            print("❌ Тест не пройден")
            sys.exit(1)
    except AssertionError as e:
        print(f"❌ Ошибка утверждения: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Неожиданная ошибка: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)