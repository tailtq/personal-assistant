import abc
from abc import abstractmethod
from typing import Union
from threading import Lock


class BaseBot(abc.ABC):
    _lock = Lock()
    _instances = {}

    def __init__(self, token: str):
        self._token = token

        # ensure the __init__ method is sequentially accessed in multi-threads environment
        with self._lock:
            # only allow one bot by one token
            if self._token not in self._instances:
                self._instances[self._token] = super().__init__()
            else:
                raise Exception("Violate singleton pattern!")

    @classmethod
    def get_bot(cls, token: str):
        if token not in cls._instances:
            cls._instances[token] = cls(token)

        return cls._instances[token]

    @abstractmethod
    def _register_events(self):
        raise NotImplementedError()

    @abstractmethod
    def on_message(self, message):
        raise NotImplementedError()

    @abstractmethod
    def on_ready(self):
        raise NotImplementedError()

    @abstractmethod
    def send_message(self, user: Union[int, object], message: str):
        raise NotImplementedError()
