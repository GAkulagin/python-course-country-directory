"""
Функции для формирования выходной информации.
"""

from decimal import ROUND_HALF_UP, Decimal
from tabulate import tabulate, SEPARATING_LINE
from collectors.models import LocationInfoDTO


class Renderer:
    """
    Генерация результата преобразования прочитанных данных.
    """

    def __init__(self, location_info: LocationInfoDTO) -> None:
        """
        Конструктор.

        :param location_info: Данные о географическом месте.
        """

        self.location_info = location_info

    async def render(self) -> None:
        """
        Форматирование прочитанных данных и вывод в консоль.

        :return: None
        """
        table = [
            ["Страна", self.location_info.location.name],
            ["Столица", self.location_info.location.capital],
            ["Координаты столицы", f"{self.location_info.location.capital_latitude}; {self.location_info.location.capital_longitude}"],
            ["Регион", self.location_info.location.subregion],
            ["Языки", await self._format_languages()],
            ["Площадь", f"{self.location_info.location.area} кв. км."],
            ["Население страны", f"{await self._format_population()} чел."],
            ["Курсы валют", await self._format_currency_rates()],
            ["Часовой пояс", self.location_info.weather.utc_timezone],
            ["", ""],
            ["Weather", ""],
            SEPARATING_LINE,
            ["Погода", self.location_info.weather.description],
            ["Температура", f"{self.location_info.weather.temp} °C"],
            ["Скорость ветра", f"{self.location_info.weather.wind_speed} м.с."],
            ["Видимость", f"{self.location_info.weather.visibility} м."],
            ["Время получения данных", self.location_info.weather.date_time.strftime('%d.%m.%Y %H:%M')]
        ]
        if len(self.location_info.country_news) > 0:
            table.extend([
                ["", ""],
                [f"Latest news about {self.location_info.location.name}", ""],
            ])
        for item in self.location_info.country_news:
            table.extend([
                SEPARATING_LINE,
                [item.title, ""],
                ["Источник", item.source],
                ["Дата публикации", item.published_at.strftime('%d.%m.%Y %H:%M')],
            ])

        print(tabulate(table, ["General", ""], tablefmt="simple"))

    async def _format_languages(self) -> str:
        """
        Форматирование информации о языках.

        :return:
        """

        return ", ".join(
            f"{item.name} ({item.native_name})"
            for item in self.location_info.location.languages
        )

    async def _format_population(self) -> str:
        """
        Форматирование информации о населении.

        :return:
        """

        # pylint: disable=C0209
        return "{:,}".format(self.location_info.location.population).replace(",", ".")

    async def _format_currency_rates(self) -> str:
        """
        Форматирование информации о курсах валют.

        :return:
        """

        return ", ".join(
            f"{currency} = {Decimal(rates).quantize(exp=Decimal('.01'), rounding=ROUND_HALF_UP)} руб."
            for currency, rates in self.location_info.currency_rates.items()
        )
