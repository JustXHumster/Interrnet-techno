"""
Решение на чистом Python без внешних библиотек.
Соответствует wemake-python-styleguide.
"""

from datetime import date, timedelta, datetime
from typing import Dict, List, Optional, Tuple


def create_source_vitrine() -> List[Dict]:
    """
    Создать исходную витрину в соответствии с таблицей 1.

    Returns:
        List[Dict]: исходные данные о режимах работы.
    """
    return [
        {
            'tab_num': 15123,
            'start_date': datetime(2020, 9, 2).date(),
            'finish_date': datetime(9999, 12, 31).date(),
            'wday_type': [0, 0, 0, 0, 0],
            'wplace_type': 0,
            'end_da': datetime(2020, 10, 31).date(),
        },
        {
            'tab_num': 16234,
            'start_date': datetime(2020, 9, 20).date(),
            'finish_date': datetime(2020, 10, 30).date(),
            'wday_type': [0, 0, 1, 1, 0],
            'wplace_type': 2,
            'end_da': None,
        },
        {
            'tab_num': 17345,
            'start_date': datetime(2020, 9, 28).date(),
            'finish_date': datetime(2020, 10, 25).date(),
            'wday_type': [1, 0, 0, 0, 0],
            'wplace_type': 2,
            'end_da': None,
        },
        {
            'tab_num': 17345,
            'start_date': datetime(2020, 10, 26).date(),
            'finish_date': datetime(2020, 12, 31).date(),
            'wday_type': [1, 1, 1, 1, 1],
            'wplace_type': 1,
            'end_da': None,
        },
        {
            'tab_num': 18456,
            'start_date': datetime(2020, 9, 2).date(),
            'finish_date': datetime(9999, 12, 31).date(),
            'wday_type': [2, 2, 2, 2, 2],
            'wplace_type': 3,
            'end_da': datetime(2020, 9, 30).date(),
        },
        {
            'tab_num': 19567,
            'start_date': datetime(2020, 9, 2).date(),
            'finish_date': datetime(2020, 12, 31).date(),
            'wday_type': [3, 3, 3, 3, 3],
            'wplace_type': 4,
            'end_da': None,
        },
    ]


def generate_date_range(
    start_date: date,
    end_date: date,
) -> List[date]:
    """
    Сгенерировать список всех дат в диапазоне.

    Args:
        start_date: начальная дата
        end_date: конечная дата

    Returns:
        List[date]: список дат
    """
    dates = []
    current_date = start_date
    while current_date <= end_date:
        dates.append(current_date)
        current_date += timedelta(days=1)
    return dates


def adjust_finish_date(
    record: Dict,
) -> date:
    """
    Скорректировать дату окончания по правилу 3.

    Args:
        record: запись о режиме работы

    Returns:
        date: скорректированная дата окончания
    """
    if (
        record['finish_date'] == datetime(9999, 12, 31).date()
        and record['end_da'] is not None
    ):
        return record['end_da']
    return record['finish_date']


def process_regular_mode(
    record: Dict,
    current_date: date,
) -> Optional[int]:
    """
    Обработать стандартные режимы (wplace_type 0,1,2).

    Args:
        record: запись о режиме работы
        current_date: текущая дата

    Returns:
        Optional[int]: флаг to_be_at_office
    """
    weekday = current_date.weekday()  # пн=0, вс=6

    # Выходные дни
    if weekday >= 5:
        return None

    # Получаем флаг для дня недели
    wday_flag = record['wday_type'][weekday]

    # 0 - офис (1), остальное - дистанция (0)
    return 1 if wday_flag == 0 else 0


def process_wplace_type_3(
    days_from_start: int,
) -> int:
    """
    Обработать режим wplace_type=3 (неделя через неделю).

    Args:
        days_from_start: количество дней от начала режима

    Returns:
        int: флаг to_be_at_office (0 - дистанция, 1 - офис)
    """
    week_num = days_from_start // 7
    # Четные недели (0,2,4...) - офис? Нет: в описании:
    # 1-я неделя - дистанция, 2-я - офис
    return 1 if (week_num % 2) == 1 else 0


def process_wplace_type_4(
    days_from_start: int,
) -> int:
    """
    Обработать режим wplace_type=4 (две недели через две).

    Args:
        days_from_start: количество дней от начала режима

    Returns:
        int: флаг to_be_at_office (0 - дистанция, 1 - офис)
    """
    week_num = days_from_start // 7
    # Первые 2 недели - дистанция, следующие 2 - офис
    two_week_block = week_num // 2
    return 1 if (two_week_block % 2) == 1 else 0


def create_target_vitrine(
    source_data: List[Dict],
) -> List[Dict]:
    """
    Сформировать целевую витрину по правилам 1-8.

    Args:
        source_data: исходная витрина

    Returns:
        List[Dict]: целевая витрина
    """
    # Правило 1: диапазон дат
    start_period = date(2020, 9, 1)
    end_period = date(2020, 12, 31)
    all_dates = generate_date_range(start_period, end_period)

    # Получаем всех уникальных сотрудников
    employees = sorted({r['tab_num'] for r in source_data})

    # Корректируем даты окончания (правило 3)
    adjusted_records = []
    for record in source_data:
        adjusted = record.copy()
        adjusted['actual_finish'] = adjust_finish_date(record)
        adjusted_records.append(adjusted)

    # Словарь для результатов: {tab_num: {date: flag}}
    results: Dict[int, Dict[date, Optional[int]]] = {}

    # Инициализируем все даты как None для каждого сотрудника
    for emp in employees:
        results[emp] = {d: None for d in all_dates}

    # Обрабатываем каждый режим
    for record in adjusted_records:
        tab_num = record['tab_num']

        # Период действия режима
        period_start = max(record['start_date'], start_period)
        period_end = min(record['actual_finish'], end_period)

        # Генерируем даты периода
        current_date = period_start
        while current_date <= period_end:
            days_from_start = (current_date - record['start_date']).days

            # Определяем флаг в зависимости от типа режима
            if record['wplace_type'] in (3, 4):
                if current_date.weekday() >= 5:  # выходной
                    flag = None
                elif record['wplace_type'] == 3:
                    flag = process_wplace_type_3(days_from_start)
                else:  # wplace_type == 4
                    flag = process_wplace_type_4(days_from_start)
            else:
                flag = process_regular_mode(record, current_date)

            # Сохраняем флаг (перезаписываем более поздними режимами)
            if flag is not None or results[tab_num][current_date] is None:
                results[tab_num][current_date] = flag

            current_date += timedelta(days=1)

    # Формируем финальную витрину
    target_vitrine = []
    for emp in employees:
        for single_date in all_dates:
            target_vitrine.append({
                'tab_num': emp,
                'ymd_date': single_date.strftime('%d.%m.%Y'),
                'to_be_at_office': results[emp][single_date],
            })

    return target_vitrine


def main() -> None:
    """Основная функция выполнения задания."""
    # Блок 1: исходная витрина
    source = create_source_vitrine()
    print('Исходная витрина сформирована')
    print(f'Количество записей: {len(source)}')

    # Блок 2: целевая витрина
    target = create_target_vitrine(source)
    print(f'Целевая витрина сформирована')
    print(f'Количество записей: {len(target)}')
    print(f'Количество сотрудников: {len({r["tab_num"] for r in target})}')
    print(f'Диапазон дат: {target[0]["ymd_date"]} - {target[-1]["ymd_date"]}')

    # Проверка контрольных точек из таблицы 3
    print('\n=== ПРОВЕРКА КОНТРОЛЬНЫХ ТОЧЕК ===')
    check_points = [
        (15123, '02.09.2020', 1),
        (16234, '23.09.2020', 0),
        (16234, '24.09.2020', 0),
        (17345, '26.10.2020', 0),
        (18456, '02.09.2020', 0),
        (18456, '07.09.2020', 1),
    ]

    # Создаем словарь для быстрого поиска
    target_dict = {(r['tab_num'], r['ymd_date']): r['to_be_at_office'] for r in target}

    for tab_num, date_str, expected in check_points:
        actual = target_dict.get((tab_num, date_str))
        status = 'OK' if actual == expected else 'ОШИБКА'
        print(f'tab_num: {tab_num}, дата: {date_str}, '
              f'ожидалось: {expected}, получено: {actual} - {status}')

    # Вывод первых 20 строк как в таблице 3
    print('\n=== ПЕРВЫЕ 20 СТРОК ЦЕЛЕВОЙ ВИТРИНЫ ===')
    for i, row in enumerate(target[:20]):
        print(f"{row['tab_num']:10} {row['ymd_date']:12} {row['to_be_at_office']}")


if __name__ == '__main__':
    main()