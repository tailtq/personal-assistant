from typing import Any

from redis import Redis
from django.conf import settings

REDIS_HOST = settings.DATABASES["redis"]["HOST"]
REDIS_PORT = settings.DATABASES["redis"]["PORT"]
REDIS_USERNAME = settings.DATABASES["redis"]["USERNAME"]
REDIS_PASSWORD = settings.DATABASES["redis"]["PASSWORD"]
REDIS_SSL = settings.DATABASES["redis"]["SSL"]
REDIS_DB = settings.DATABASES["redis"]["DB"]
REDIS_CLIENT = Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    username=REDIS_USERNAME,
    password=REDIS_PASSWORD,
    db=REDIS_DB,
    ssl=REDIS_SSL,
    ssl_cert_reqs=None,
)


class RedisMessageQueueService:
    def __init__(self, queue_name: str):
        self._queue_name = queue_name

    def push(self, value: Any) -> None:
        REDIS_CLIENT.rpush(self._queue_name, value)

    def pull(self) -> Any:
        return REDIS_CLIENT.rpop(self._queue_name)

    def is_empty(self) -> bool:
        return not bool(REDIS_CLIENT.llen(self._queue_name))
