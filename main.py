import function
while True:
    try:
        expression = input('Введите выражение (например, "2 + 3 * 4") или "exit" для выхода: ')
        if not expression.strip():
            continue

        # Проверяем, является ли ввод командой выхода
        if expression.lower() in ['exit', 'выход']:
            print("Выход из программы")
            break

        # Токенизируем выражение
        tokens = function.tokenize_expression(expression)

        if not tokens:
            continue

        # Преобразуем в ОПЗ с помощью существующей функции
        rpn_tokens = function.to_rpn(tokens)

        # Вычисляем результат с помощью существующей функции
        result = function.eval_rpn(rpn_tokens)

        # Округляем результат до тысячных для красивого вывода
        rounded_result = function.round_decimal(result, 3)
        print(f"Результат: {rounded_result}")

    except ValueError as e:
        print(f"Ошибка в выражении: {e}")
    except ZeroDivisionError:
        print("Ошибка: Деление на ноль")
    except Exception as e:
        print(f"Ошибка: {e}")
