from itertools import count


class Data:
    """Класс реализующий объект пакета данных"""
    
    def __init__(self, data: str, ip: int):
        self.data: str = data
        self.receiver_ip: int = ip


class Server:
    
    next_ip = count()

    def __init__(self):
        self.__ip: int = next(self.next_ip)
        self.__router: Router = None
        self.buffer: list[Data] = []


    def get_ip(self):
        return self.__ip


    @property
    def router(self):
        return self.__router


    @router.setter
    def router(self, router):
        self.__router = router


    def add_to_buffer(self, data: Data):
        self.buffer.append(data)


    def send_data(self, data: Data):
        if self.router:
            self.router.add_to_buffer(data)
        else:
            raise ConnectionError("Server is not connected to the router")
    

    def get_data(self):
        data = self.buffer.copy()
        self.buffer.clear()
        return data


class Router:
    
    def __init__(self):
        self.servers: dict[int, Server] = dict()
        self.buffer: list[Data] = []
    
    def link(self, server):
        self.servers[server.get_ip()] = server
        server.router = self

    def unlink(self, server):
        server.router = None
        del self.servers[server.get_ip()]

    def add_to_buffer(self, data):
        self.buffer.append(data)

    def send_data(self):
        while self.buffer:
            data = self.buffer.pop(0)   # не эффективно O(N^2)
            receiver_ip = data.receiver_ip
            if receiver_ip in self.servers:
                self.servers[receiver_ip].add_to_buffer(data)
