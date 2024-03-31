"""Домашнє завдання #5
Напишіть консольну утиліту, яка повертає курс EUR та USD ПриватБанку протягом
останніх кількох днів. Встановіть обмеження, що в утиліті можна дізнатися
курс валют не більше, ніж за останні 10 днів.
Для запиту до АПІ використовуйте Aiohttp client.
Дотримуйтесь принципів SOLID під час написання завдання.
Обробляйте коректно помилки при мережевих запитах."""

# main.py
import logging
import asyncio
import aiohttp
import platform
from pprint import pprint

from limits_date import parser, clear_date
from proccesing_date import list_dates


async def index(session, _date):
    url = "https://api.privatbank.ua/p24api/exchange_rates?json&date=" + _date
    async with session.get(url) as response:
        print("receiving data for:", _date)
        try:
            if response.status == 200:
                return await response.json()
            logging.error(f"Error status {response.status} for {url}")
        except aiohttp.ClientConnectionError as e:
            logging.error(f"Connection error {url} as {e}")
        return None


async def gather_session(dates):
    async with aiohttp.ClientSession() as session:
        _session_list = []
        for _date in dates:
            _session_list.append(index(session, _date))

        return await asyncio.gather(*_session_list, return_exceptions=True)


def extract_currency_data(data, currencies):
    currency_data = {}
    for currency in currencies:
        for rate in data['exchangeRate']:
            if rate['currency'] == currency:
                currency_data[currency] = {
                    'sale': rate['saleRate'],
                    'purchase': rate['purchaseRate']
                }
                break
    return currency_data


async def main():
    currencies = ["EUR", "USD"]

    _date, _days = await parser()

    dates = list_dates(_date, _days)

    result = await gather_session(dates)

    output_data = []
    for date_data in result:
        if date_data is not None:
            currency_data = extract_currency_data(date_data, currencies)
            output_data.append({date_data['date']: currency_data})

    pprint(output_data)  # Використання pprint для красивого виводу даних


if __name__ == "__main__":
    if platform.system() == "Windows":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    asyncio.run(main())






