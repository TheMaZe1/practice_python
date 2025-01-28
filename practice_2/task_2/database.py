import abc
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

from config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER
from models import Base, SpimexTrade


class Repository(abc.ABC):
    """Интерфейс для репозитория"""

    @abc.abstractmethod
    def add(self, entity: list[SpimexTrade]):
        raise NotImplementedError
    

    @abc.abstractmethod
    def update(self, id_: id):
        raise NotImplementedError
    

    @abc.abstractmethod
    def remove(self, id_: id):
        raise NotImplementedError
    

    @abc.abstractmethod
    def get_by_id(self, id_: id):
        raise NotImplementedError


class SQLAlchemyRepository(Repository):

    def __init__(self) -> None:
        self.engine = create_engine(f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}", echo=True)
        Base.metadata.create_all(self.engine)

    def add(self, entity: list[SpimexTrade]) -> None:
        with Session(bind=self.engine) as s:
            for ent in entity:
                s.add(ent)
            s.commit()

    def update(self, id_: id):
        ...
    
    def remove(self, id_: id):
        ...

    def get_by_id(self, id_: id):
        ...