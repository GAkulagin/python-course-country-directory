"""
Функции для взаимодействия с внешним сервисом-провайдером новостей.
"""
from datetime import datetime
from http import HTTPStatus
from typing import Optional

import aiohttp

from clients.base import BaseClient
from logger import trace_config
from settings import API_KEY_NEWSPORTAL


class NewsClient(BaseClient):
    """
    Реализация функций для взаимодействия с внешним сервисом-провайдером новостей.
    """

    async def get_base_url(self) -> str:
        return "https://newsapi.org/v2/everything"

    async def _request(self, endpoint: str) -> Optional[dict]:
        async with aiohttp.ClientSession(trace_configs=[trace_config]) as session:
            async with session.get(endpoint) as response:
                if response.status == HTTPStatus.OK:
                    return await response.json()

                return None

    async def get_news(self, country: str) -> Optional[dict]:
        """
         Получение новостей о стране за сегодня.

        :param country: Страна
        :return: JSON-данные о новостях
        """

        return await self._request(
            f"{await self.get_base_url()}?q={country}&sortBy=publishedAt&apiKey={API_KEY_NEWSPORTAL}")
