import abc
from abc import abstractmethod

from discord import Client


class BaseBot(abc.ABC):
    # def __init__(self, bot):
    #     self.bot: Client = bot

    @abstractmethod
    def publish_message(self):
        raise NotImplementedError()

    @abstractmethod
    def publish_embedded_message(self):
        pass

    @abstractmethod
    def listen_message(self):
        pass
