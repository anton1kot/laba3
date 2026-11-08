from .errors import DuplicateIdError, NotFoundError


class Catalog:
    def __init__(self):
        self._items = {}  # словарь для O(1) поиска по ID
        self._order = []  # список ID для детерминированной итерации (порядок добавления)

    def add(self, item):
        # добавление книги, проверка дубликата
        if item.id in self._items:
            raise DuplicateIdError(f'duplicate id: {item.id}')
        self._items[item.id] = item
        self._order.append(item.id)

    def get(self, item_id):
        # получение по ID (O(1))
        if item_id not in self._items:
            raise NotFoundError(f'not found: {item_id}')
        return self._items[item_id]

    def remove(self, id):
        # удаление по ID
        if id not in self._items:
            raise NotFoundError(f'not found: {id}')
        del self._items[id]
        self._order.remove(id)

    def find_by_category(self, category):
        # поиск по категории (O(n)), возвращает копию списка
        res = []
        for id in self._order:
            if self._items[id].category == category:
                res.append(self._items[id])
        return list(res)

    def find_by_name(self, book_name):
        # поиск по названию, O(n), возвращает копию
        res = []
        book_name = book_name.lower()
        for id in self._order:
            if book_name in self._items[id].name.lower():
                res.append(self._items[id])
        return list(res)

    def __len__(self):
        return len(self._items)

    def __iter__(self):
        # итерация в порядке добавления
        for id in self._order:
            yield self._items[id]

    def __contains__(self, item_id):
        return item_id in self._items
