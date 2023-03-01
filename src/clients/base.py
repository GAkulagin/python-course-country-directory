"""
Базовые функции для клиентов внешних сервисов.
"""

from abc import ABC, abstractmethod
from typing import Optional


class BaseClient(ABC):
    """
    Базовый класс, реализующий интерфейс для клиентов.
    """

    @abstractmethod
    async def get_base_url(self) -> str:
        """
        Получение базового URL для запросов.

        :return:
        """

    @abstractmethod
    async def _request(self, endpoint: str) -> Optional[dict]:
        """
        Формирование и выполнение запроса.

        :param endpoint:
        :return: JSON
        """
