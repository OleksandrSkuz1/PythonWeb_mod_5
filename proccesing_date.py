'''обробка введення дати:
    формується список дат для реквесту на сайт приват-банку
    перевіряється коректність введення дати
    в разі помилок вводу, формується відповідне повідомлення
    введена дата приводиться до формату "dd.mm.yyy"'''

from datetime import date, datetime, timedelta
import sys

ERROR_DATA = "> wrong data: "
ERROR_FORMAT_DATE = " - date format must be 'dd.mm.yyyy' or 'yyyy.mm.dd'"
ERROR_WRONG_DATE = " - the entered date is older than today"


def _date_to_str(_date) -> str:
    if isinstance(_date, type(date.today())):
        _date = str(_date)
    return _date


def _switch_to_dmy(_date) -> str:
    '''switch "yyyy.mm.dd" to "dd.mm.yyyy"'''
    try:
        if all([_date[4] == _date[7] == "."]):
            _date = _date[8:] + "." + _date[5:7] + "." + _date[0:4]
    except IndexError:
        sys.exit(ERROR_DATA + _date + ERROR_FORMAT_DATE)
    return _date


def _normalize_date(_date) -> str:
    return _switch_to_dmy(_date_to_str(_date).replace("-", ".").replace("/", "."))


def clear_date(_date) -> str:
    """Check if the entered date is correct and not greater than today"""

    n_date = _normalize_date(_date)

    try:
        if datetime.strptime(n_date, "%d.%m.%Y").date() > datetime.now().date():
            sys.exit(ERROR_DATA + _date + ERROR_WRONG_DATE)
    except ValueError:
        sys.exit(ERROR_DATA + _date + ERROR_FORMAT_DATE)

    return n_date


def list_dates(_date, _nums) -> list:
    """make list(dates)"""

    dates = []

    date_datetime = datetime.strptime(_date, "%d.%m.%Y").date()

    while _nums > 0:
        dates.append(date_datetime.strftime("%d.%m.%Y"))
        date_datetime -= timedelta(1)
        _nums -= 1

    return dates


if __name__ == "__main__":
    print(" === date_processing === ")
    print(list_dates(clear_date("5/12-2023"), 4))

