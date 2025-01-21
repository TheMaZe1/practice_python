from typing import Optional, Self


class ObjList:
    """Класс реализующий объект связного списка"""

    def __init__(self, data: str) -> None:
        self.__data: str = data
        self.__next: Optional[Self] = None
        self.__prev: Optional[Self] = None


    def get_next(self) -> Optional[Self]:
        return self.__next
    

    def set_next(self, obj: Optional[Self]) -> None:
        self.__next = obj


    def get_prev(self) -> Optional[Self]:
        return self.__prev
    

    def set_prev(self, obj: Optional[Self]) -> None:
        self.__prev = obj


    def get_data(self) -> str:
        return self.__data
    

    def set_data(self, data: str) -> None:
        self.__data = data


class LinkedList:
    """Класс реализующий связный список"""

    def __init__(self) -> None:
        self.head: Optional[ObjList] = None
        self.tail: Optional[ObjList] = None


    def add_object(self, obj: ObjList) -> None:
        """Добавить объект в конец списка"""
        obj.set_prev(None)
        obj.set_next(None)

        if not self.head:
            self.head = obj
            self.tail = obj
        else:
            self.tail.set_next(obj)
            obj.set_prev(self.tail)
            self.tail = obj
            

    def remove_obj(self) -> None:
        """Удалить объект из конца списка. Бросает исключение если список пуст"""
        if not self.head:
            raise IndexError("Linked list is empty")
        else:
            obj = self.tail
            self.tail = obj.get_prev()
            self.tail.set_next(None)
            del obj


    def get_data(self) -> list[str]:
        """Возвращает список из строк поля data для всех объектов списка"""
        current = self.head
        data = []
        while current != None:
            data.append(current.get_data())
            current = current.get_next()
        return data
    