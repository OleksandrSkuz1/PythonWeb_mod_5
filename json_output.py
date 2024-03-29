def print_table(data):
    """
    Функція для виведення даних у вигляді таблиці.
    Вхідні параметри:
    - data: дані, які потрібно вивести
    """
    output = []
    for date, currencies_data in data.items():
        output_data = {date: {}}
        for currency, rates in currencies_data.items():
            output_data[date][currency] = {
                'sale': rates['saleRate'],
                'purchase': rates['purchaseRate']
            }
        output.append(output_data)
    print(output)

# Цей код буде виконуватися лише при виклику цього модуля як головного
if __name__ == "__main__":
    # Додатковий код для тестування функцій
    pass


