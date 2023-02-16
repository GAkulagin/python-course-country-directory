"""
Функции для взаимодействия с внешним сервисом-провайдером данных о курсах валют.
"""
from http import HTTPStatus
from typing import Optional

import aiohttp

from clients.base import BaseClient
from logger import trace_config
from settings import API_KEY_APILAYER


class CurrencyClient(BaseClient):
    """
    Реализация функций для взаимодействия с внешним сервисом-провайдером данных о курсах валют.
    """

    async def get_base_url(self) -> str:
        return "https://api.apilayer.com/fixer/latest"

    async def _request(self, endpoint: str) -> Optional[dict]:

        # формирование заголовков запроса
        headers = {"apikey": API_KEY_APILAYER}

        async with aiohttp.ClientSession(trace_configs=[trace_config]) as session:
            async with session.get(endpoint, headers=headers) as response:
                if response.status == HTTPStatus.OK:
                    return await response.json()

                return None

    async def get_rates(self, base: str = "rub") -> Optional[dict]:
        """
         Получение данных о курсах валют.

        :param base: Базовая валюта
        :return: JSON-данные о курсах валют
        """

        return await self._request(f"{await self.get_base_url()}?base={base}")
