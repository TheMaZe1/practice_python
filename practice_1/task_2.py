import random


class Cell:
    """Класс реализующий объект клетки"""

    def __init__(self, around_mines: int = 0, mine: bool = False):
        self.__around_mines: int = around_mines
        self.__mine: bool = mine
        self.__fl_open: bool = True # Все клетки открыты для демонстрации сгенерированного поля

    
    @property
    def around_mines(self) -> int:
        return self.__around_mines
    

    @around_mines.setter
    def around_mines(self, around_mines: int) -> None:
        self.__around_mines = around_mines


    @property
    def mine(self) -> int:
        return self.__mine
    

    @mine.setter
    def mine(self, mine: bool) -> None:
        self.__mine = mine


    @property
    def fl_open(self) -> bool:
        return self.__fl_open
    

    @fl_open.setter
    def fl_open(self, fl_open: bool) -> None:
        self.__fl_open = fl_open


class GamePole:
    """Класс реализующий игрове поле"""

    def __init__(self, N: int, M: int):
        self.__N = N
        self.__M = M
        self.init()


    def is_mine(self, i: int, j: int) -> bool:
        return self.pole[i][j].mine
    

    def __generate_mines(self):
        """Расставляет мины по полю случайным образом"""
        mines = random.sample(range(0, self.__N**2), self.__M)
        for mine in mines:
            self.pole[mine // self.__N][mine % self.__N].mine = True


    def __count_mines_around(self, i: int, j: int):
        """Считает кол-во мин вокруг клетки"""
        directions = ((0, -1), (-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1))
        cell = self.pole[i][j]
        count_mines = 0
        if not self.is_mine(i, j):
            for direction in directions:
                i_neighbor = i + direction[0]
                j_neighbor = j + direction[1]
                if 0 <= i_neighbor < self.__N and 0 <= j_neighbor < self.__N:
                    if self.pole[i_neighbor][j_neighbor].mine:
                        count_mines += 1
            cell.around_mines = count_mines


    def init(self):
        """Генерация игрового поля"""
        self.pole = [[Cell() for _ in range(self.__N)] for _ in range(self.__N)]
        self.__generate_mines()

        for i in range(0, self.__N):
            for j in range(0, self.__N):
                self.__count_mines_around(i,j)


    def open_cell(self, i: int, j: int):
        self.pole[i][j].fl_open = True

    
    def show(self):
        for i in self.pole:
            for j in i:
                if not j.fl_open:
                    print('#', end=' ')
                elif j.mine:
                    print('*', end=' ')
                else:
                    print(j.around_mines, end=' ')
            print()
