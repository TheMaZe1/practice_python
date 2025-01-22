import random

random.seed(123)

class Cell:
    """Класс реализующий объект клетки"""

    def __init__(self, around_mines: int = 0, mine: bool = False) -> None:
        self.__around_mines: int = around_mines
        self.__mine: bool = mine
        self.__fl_open: bool = False
        self.__flag = False

    
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


    @property
    def flag(self) -> bool:
        return self.__flag
    

    @flag.setter
    def flag(self, flag: bool) -> None:
        self.__flag = flag



class GamePole:
    """Класс реализующий игрове поле"""

    DIRECTIONS = ((0, -1), (-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1)) # направления для поиска соседей клетки

    def __init__(self, size: int, mines: int) -> None:
        self.__size: int = size
        self.__mines: int = mines
        self.init()


    @property
    def size(self) -> int:
        return self.__size
    
    @property
    def mines(self) -> int:
        return self.__mines
    

    def __generate_mines(self) -> None:
        """Расставляет мины по полю случайным образом"""
        mines = random.sample(range(0, self.__size**2), self.__mines)
        for mine in mines:
            self.pole[mine // self.__size][mine % self.__size].mine = True


    def __count_mines_around(self, i: int, j: int) -> None:
        """Считает кол-во мин вокруг клетки"""
        cell = self.pole[i][j]
        count_mines = 0
        if not cell.mine:
            for direction in self.DIRECTIONS:
                i_neighbor = i + direction[0]
                j_neighbor = j + direction[1]
                if 0 <= i_neighbor < self.__size and 0 <= j_neighbor < self.__size:
                    if self.pole[i_neighbor][j_neighbor].mine:
                        count_mines += 1
            cell.around_mines = count_mines


    def init(self) -> None:
        """Генерация игрового поля"""
        self.pole = [[Cell() for _ in range(self.__size)] for _ in range(self.__size)]
        self.__generate_mines()

        for i in range(0, self.__size):
            for j in range(0, self.__size):
                self.__count_mines_around(i,j)


    def open_cell(self, i: int, j: int) -> None:
        self.pole[i][j].fl_open = True


    def flag(self, i: int, j: int) -> None:
        """Устанавливает или снивает флаг с клетки"""
        self.pole[i][j].flag = not self.pole[i][j].flag

    
    def show(self, _all: bool=False) -> None:
        print(' '*2, *range(0, self.size), sep=' ')
        print(' '*2, '-'*(self.size*2-1), sep=' ')
        for i, line in enumerate(self.pole):
            print(str(i) + '|', end=' ')
            for j in line:
                if not _all and not j.fl_open:
                    if j.flag:
                        print('F', end=' ')
                    else:
                        print('#', end=' ')
                elif j.mine:
                    print('*', end=' ')
                else:
                    print(j.around_mines, end=' ')
            print()


class Saper:
    """Класс игры в сапёр"""

    def __init__(self, size: int, mines: int) -> None:
        self.__game_pole: GamePole = GamePole(size, mines)
        self.__remaining_cells: set[Cell] = set()  # множество клеток которые осталось открыть для победы
        for line in self.__game_pole.pole:
            for cell in line:
                if not cell.mine:
                    self.__remaining_cells.add(cell)


    def __validate_index(self, i: int, j: int) -> None:
        if not (0 <= i < self.__game_pole.size and 0 <= j < self.__game_pole.size):
            raise IndexError("Недопустимый номер клетки")
        

    def __open_cell(self, i: int, j: int) -> None:
        cell: Cell = self.__game_pole.pole[i][j]

        if not cell.mine and not cell.fl_open:
            self.__game_pole.open_cell(i,j)
            self.__remaining_cells.discard(cell)
            if cell.around_mines == 0:
                for direction in self.__game_pole.DIRECTIONS:
                    i_neighbor = i + direction[0]
                    j_neighbor = j + direction[1]
                    if 0 <= i_neighbor < self.__game_pole.size and 0 <= j_neighbor < self.__game_pole.size:
                        self.__open_cell(i_neighbor, j_neighbor)
    

    def play(self) -> None:
        while True:
            self.__game_pole.show()
            try:
                i, j = map(int, input("Введите номер клетки(индекс строки и столбца через пробел): ").split())
                self.__validate_index(i,j)

                number = int(input("1. Открыть клекту\n2. Поставить\снять флаг\nВыберите пункт: "))
            except IndexError:
                print("Неверный номер клетки")
                continue
            except ValueError:
                print("Некореектный ввод")
                continue
            
            if self.__game_pole.pole[i][j].fl_open:
                print("Клетка уже открыта")
                continue

            if number == 1:
                if self.__game_pole.pole[i][j].mine:
                    self.__game_pole.show(_all=True)
                    print("Вы проиграли(")
                    return
                else:
                    self.__open_cell(i,j)
                    if len(self.__remaining_cells) == 0:
                        self.__game_pole.show()
                        print("Вы выиграли!!!")
                        return
            elif number == 2:
                self.__game_pole.flag(i,j)
            else:
                print("Отсутсвует данный пункт меню")


s = Saper(5, 2)
s.play()

    