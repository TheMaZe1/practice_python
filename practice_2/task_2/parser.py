import requests
import xlrd

import datetime
from calendar import monthrange

from database import Repository, SQLAlchemyRepository
from models import SpimexTrade


class NotFoundException(Exception):
    pass


class Parser:
    """Класс парсит данные отчетов за указзаный год, начиная с определенного месяца и дня. Сохраняет их в БД"""

    base_link = 'https://spimex.com/upload/reports/oil_xls/oil_xls_'
    file_name = 'practice_2/task_2/parse_file.xls'

    def __init__(self, year: int, repo: Repository, start_month: int=1, start_day: int=1) -> None:
        self.year: int = year
        self.start_month: int = start_month
        self.start_day: int = start_day
        self.repo = repo

    
    def _download(self, date: datetime.date) -> None:
        """Скачивает файл отчета за указанную дату и сохраняет его с именем <file_name>.
        Если файл за указаную дату не найден, кидает исключение
        """
        str_date = date.strftime('%Y%m%d')

        response = requests.get(self.base_link+f'{str_date}162000.xls')
        if response.status_code == 404:
            raise NotFoundException
        with open(self.file_name, 'wb') as f:
            f.write(response.content)

    @classmethod
    def _map_row_to_spimex_trade(cls, row: list, date: datetime) -> SpimexTrade:
        """Конвертирует строку XLS файла с данными в объект для сохранения в БД"""
        return SpimexTrade(
            exchange_product_id = row[1].value,
            exchange_product_name = row[2].value,
            oil_id = row[1].value[:4],
            delivery_basis_id = row[1].value[4:7],
            delivery_basis_name = row[3].value,
            delivery_type_id = row[1].value[-1],
            volume = row[4].value,
            total = row[5].value,
            count = row[-1].value,
            date = date,
            created_on = datetime.datetime.now(),
            updated_on = datetime.datetime.now()

    )

    
    def parse(self) -> None:
        """Парсит данные отчета за каждый день в заданном году, если отчет существует сохраняет в БД"""
        for month in range(self.start_month, 13):
            for day in range(self.start_day, monthrange(self.year, month)[1] + 1):
                try:
                    date: datetime = datetime.date(self.year, month, day)
                    start_row: int = 0
                    spimex_trades: list[SpimexTrade] = []
                    
                    self._download(date)
                    wb = xlrd.open_workbook(self.file_name)
                    ws = wb.sheet_by_index(0)
                    
                    for row in range(ws.nrows):                             # Ищем на какой строчке начинаются данные
                        if ws.row(row)[1].value == 'Единица измерения: Метрическая тонна':
                            start_row = row + 3                              # Данные начинаются на 2 строчки ниже строки 'Единица измерения: Метрическая тонна'
                            break

                    while ws.row(start_row)[1].value != 'Итого:':
                        if ws.row(start_row)[-1].value != '-':
                            spimex_trades.append(self._map_row_to_spimex_trade(ws.row(start_row), datetime.date(self.year, month, day)))
                        start_row += 1
                    self.repo.add(spimex_trades)
                except NotFoundException:
                    continue
                except Exception as e:
                    print(f"Последний сохраненный день: {date - datetime.timedelta(days=1)}")
                    raise e
                


    
    

if __name__ == '__main__':
    sqlrepo = SQLAlchemyRepository()
    p = Parser(2023, sqlrepo)
    p.parse()
