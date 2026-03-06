class TreeStore:
    def __init__(self, items):
        # Сохраняем исходный массив
        self._items = items.copy()

        # Создаем словарь для быстрого доступа к элементам по id
        self._items_by_id = {}

        # Создаем словарь для хранения дочерних элементов по parent
        self._children_by_parent = {}

        # Заполняем структуры данных за один проход
        for item in items:
            # Сохраняем элемент в словарь по id
            item_id = item["id"]
            self._items_by_id[item_id] = item

            # Добавляем элемент в список дочерних для его parent
            parent = item["parent"]
            if parent not in self._children_by_parent:
                self._children_by_parent[parent] = []
            self._children_by_parent[parent].append(item)

    def getAll(self):
        """Возвращает исходный массив элементов"""
        return self._items.copy()

    def getItem(self, id):
        """Возвращает элемент по его id"""
        return self._items_by_id.get(id)

    def getChildren(self, id):
        """Возвращает массив дочерних элементов для указанного id"""
        return self._children_by_parent.get(id, []).copy()

    def getAllParents(self, id):
        """Возвращает массив родительских элементов от указанного элемента до корня"""
        parents = []
        current_id = id

        # Поднимаемся по дереву вверх пока не достигнем корня
        while True:
            # Получаем текущий элемент
            current_item = self.getItem(current_id)
            if not current_item:
                break

            parent_id = current_item["parent"]

            # Получаем родительский элемент
            parent_item = self.getItem(parent_id)
            if not parent_item:
                break

            # Добавляем родителя в начало списка
            parents.append(parent_item)

            # Переходим к родителю
            current_id = parent_id

        return parents


# Исходные данные
items = [
    {"id": 1, "parent": "root"},
    {"id": 2, "parent": 1, "type": "test"},
    {"id": 3, "parent": 1, "type": "test"},
    {"id": 4, "parent": 2, "type": "test"},
    {"id": 5, "parent": 2, "type": "test"},
    {"id": 6, "parent": 2, "type": "test"},
    {"id": 7, "parent": 4, "type": None},
    {"id": 8, "parent": 4, "type": None}
]

ts = TreeStore(items)

# Примеры использования
print("getAll():", ts.getAll())
print("\ngetItem(7):", ts.getItem(7))
print("\ngetChildren(4):", ts.getChildren(4))
print("getChildren(5):", ts.getChildren(5))
print("\ngetAllParents(7):", ts.getAllParents(7))