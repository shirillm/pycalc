import math

# приоритеты операторов
PRIORITY = {
    '+': 1,
    '-': 1,
    '*': 2,
    '/': 2,
    '%': 2,
    '**': 3,  # возведение в степень
    'u-': 4  # унарный минус
}

def to_rpn(tokens):
    """
    Расширенный алгоритм ОПН с поддержкой математических функций
    """
    output = []
    stack = []

    for i, token in enumerate(tokens):
        if token.replace('.', '').isdigit() and token.count('.') <= 1:
            # Это число - сразу в результат
            output.append(token)

        elif token.lower() in ['pi', 'e']:
            # Математическая константа - сразу в результат
            output.append(token.lower())

        elif token.lower() in ['sin', 'cos', 'tan']:
            # Математическая функция - в стек
            stack.append(token.upper())  # SIN, COS, TAN

        elif token in PRIORITY:
            # Оператор - обрабатываем приоритеты
            if token == '-' and (i == 0 or tokens[i-1] in PRIORITY or tokens[i-1] == '('):
                token = 'u-'

            while (stack and stack[-1] in PRIORITY and
                   PRIORITY[stack[-1]] >= PRIORITY[token]):
                output.append(stack.pop())

            stack.append(token)

        elif token == '(':
            stack.append(token)
        elif token == ')':
            while stack and stack[-1] != '(':
                output.append(stack.pop())
            if stack:
                stack.pop()  # убираем '('

            # Если после скобки функция - выталкиваем её
            if stack and stack[-1] in ['SIN', 'COS', 'TAN']:
                output.append(stack.pop())

    # Выталкиваем все оставшиеся операторы и функции
    while stack:
        output.append(stack.pop())

    print(f"ОПН: {' '.join(output)}")
    return output
def eval_rpn(rpn_tokens):
    """
    Вычисляет выражение в обратной польской нотации с поддержкой функций
    """
    stack = []

    for token in rpn_tokens:
        if token.replace('.', '').isdigit() and token.count('.') <= 1:
            # Это число
            number = float(token)
            stack.append(number)

        elif token.lower() == 'pi':
            # Константа пи
            stack.append(math.pi)

        elif token.lower() == 'e':
            # Константа e
            stack.append(math.e)

        elif token == 'u-':
            # Унарный минус
            if not stack:
                raise ValueError("Недостаточно операндов для унарного минуса")
            val = stack.pop()
            stack.append(-val)

        elif token in ['SIN', 'COS', 'TAN']:
            # Тригонометрические функции
            if not stack:
                raise ValueError(f"Недостаточно аргументов для функции {token}")

            arg = stack.pop()  # Берем аргумент функции

            print(f"Выполняем функцию: {token}({arg})")

            if token == 'SIN':
                result = math.sin(arg)  # Синус в радианах
            elif token == 'COS':
                result = math.cos(arg)  # Косинус в радианах
            elif token == 'TAN':
                result = math.tan(arg)  # Тангенс в радианах
            else:
                raise ValueError(f"Неизвестная функция: {token}")

            stack.append(result)
            print(f"Результат функции: {result}")

        else:
            # Бинарные операторы
            if len(stack) < 2:
                raise ValueError("Недостаточно операндов для операции")

            b = stack.pop()
            a = stack.pop()

            print(f"Выполняем операцию: {a} {token} {b}")

            if token == '+':
                result = a + b
            elif token == '-':
                result = a - b
            elif token == '*':
                result = a * b
            elif token == '/':
                if b == 0:
                    raise ZeroDivisionError("Деление на ноль")
                result = a / b
            elif token == '%':
                if b == 0:
                    raise ZeroDivisionError("Деление на ноль")
                result = a % b
            elif token == '**':
                result = a ** b
            else:
                raise ValueError(f"Неизвестный оператор: {token}")

            stack.append(result)
            print(f"Результат операции: {result}")

    if len(stack) != 1:
        raise ValueError("Неверное выражение")

    return stack[0]
def calced(first,operation,second):
#Операции
    if operation=='+':
        print(first+second)
    if operation=='-':
        print(first-second)
    if operation=='/':
        if second==0:
            print('Деление на 0 запрещено.')
        else:
            print(round(first/second,5)) #Округление до тысячных
    if operation=='%':
        print(first%second)
def tokenize_expression(expr):
#   Разбивает математическое выражение на токены для новичков
#
#    Поддерживает:
#    - Числа: 2.5, 3.14
#    - Операторы: +, -, *, /, **, %
#    - Функции: sin, cos, tan (на английском)
#    - Константы: pi, e
#   - Скобки: (, )
#    Пример: "sin(pi/4) + cos(0)" -> ["sin", "(", "pi", "/", "4", ")", "+", "cos", "(", "0", ")"]
  
    # tokens - список для хранения найденных токенов
    tokens = []
    # current - для накопления числа или слова
    current = ""
    # i - индекс текущего символа
    i = 0

    # Проходим по каждому символу в выражении
    while i < len(expr):
        char = expr[i]  # Текущий символ

        if char.isdigit() or char == '.':
            # Это цифра или точка - часть числа
            current += char
            i += 1

        elif char.isalpha():
            # Это буква - может быть функцией или константой
            current += char
            i += 1

            # Проверяем, не закончилась ли функция/константа
            while i < len(expr) and (expr[i].isalpha() or expr[i].isdigit()):
                current += expr[i]
                i += 1

            # Проверяем, является ли это математической функцией или константой
            if current.lower() in ['sin', 'cos', 'tan']:
                tokens.append(current.lower())
                print(f"Найдена функция: {current.lower()}")
            elif current.lower() in ['pi', 'e']:
                tokens.append(current.lower())
                print(f"Найдена константа: {current.lower()}")
            else:
                # Неизвестное слово
                tokens.append(current)
                print(f"Неизвестное слово: {current}")

            current = ""

        elif char == '*' and i + 1 < len(expr) and expr[i + 1] == '*':
            # Нашли оператор возведения в степень **
            if current:
                tokens.append(current)
                current = ""
            tokens.append('**')
            i += 2

        elif char in '+-*/%()':
            # Это оператор или скобка
            if current:
                tokens.append(current)
                current = ""
            tokens.append(char)
            i += 1

        elif char == ' ':
            # Пробел - разделитель токенов
            if current:
                tokens.append(current)
                current = ""
            i += 1
        else:
            # Неизвестный символ
            if current:
                tokens.append(current)
                current = ""
            tokens.append(char)
            i += 1

    # Не забываем сохранить последнее накопленное
    if current:
        tokens.append(current)

    print(f"Токены: {tokens}")
    return tokens

def round_decimal(number, decimals=3): #округление
    if not isinstance(number, (int, float)):
        return number

    # Умножаем на 10^decimals, округляем, делим обратно
    multiplier = 10 ** decimals
    return round(number * multiplier) / multiplier
