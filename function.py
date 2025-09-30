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

def to_rpn(tokens): #опз
    # output - выходная очередь для результата
    output = []
    # stack - стек для операторов
    stack = []

    # Проходим по каждому токену
    for i, token in enumerate(tokens):
        if token.replace('.', '').isdigit() and token.count('.') <= 1:
            # Это число - сразу отправляем в результат
            output.append(token)
            print(f"Число {token} добавлено в результат")

        elif token in PRIORITY:
            # Это оператор - обрабатываем приоритеты
            # Проверяем унарный минус (если минус в начале или после оператора)
            if token == '-' and (i == 0 or tokens[i-1] in PRIORITY or tokens[i-1] == '('):
                token = 'u-'  # Помечаем как унарный минус

            # Пока в стеке есть операторы с большим или равным приоритетом
            while (stack and stack[-1] in PRIORITY and
                   PRIORITY[stack[-1]] >= PRIORITY[token]):
                # Вытаскиваем оператор из стека в результат
                output.append(stack.pop())

            # Кладем текущий оператор в стек
            stack.append(token)
            print(f"Оператор {token} положен в стек")

        elif token == '(':
            # Открывающая скобка - в стек
            stack.append(token)
        elif token == ')':
            # Закрывающая скобка - выталкиваем все до открывающей
            while stack and stack[-1] != '(':
                output.append(stack.pop())
            stack.pop()  # убираем саму '('

    # Выталкиваем все оставшиеся операторы из стека
    while stack:
        output.append(stack.pop())

    print(f"Результат ОПН: {' '.join(output)}")
    return output
def eval_rpn(rpn_tokens):
    """
    Вычисляет выражение в обратной польской нотации
    Работает как стековый калькулятор для новичков
    """
    # Создаем пустой стек для хранения чисел
    stack = []

    # Проходим по каждому токену в выражении
    for token in rpn_tokens:
        if token.replace('.', '').isdigit() and token.count('.') <= 1:
            # Это число (может быть дробным)
            # Преобразуем строку в число с плавающей точкой
            number = float(token)
            stack.append(number)
            print(f"Положили в стек число: {number}")

        elif token == 'u-':
            # Унарный минус (отрицательное число)
            if not stack:
                raise ValueError("Недостаточно операндов для унарного минуса")
            val = stack.pop()  # Берем последнее число
            result = -val       # Делаем его отрицательным
            stack.append(result)  # Кладем обратно в стек
            print(f"Унарный минус: {val} -> {result}")

        else:
            # Это оператор (+, -, *, /, %, **)
            if len(stack) < 2:
                raise ValueError("Недостаточно операндов для операции")

            # Берем два последних числа из стека
            b = stack.pop()  # Второе число
            a = stack.pop()  # Первое число

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
                result = a % b  # Остаток от деления
            elif token == '**':
                result = a ** b  # Возведение в степень
            else:
                raise ValueError(f"Неизвестный оператор: {token}")

            stack.append(result)
            print(f"Результат: {result}")

    # В конце в стеке должно остаться только одно число
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
    """
    Разбивает математическое выражение на токены для новичков

    Пример: "2.5 + 3.7 * 2" -> ["2.5", "+", "3.7", "*", "2"]
    """
    # tokens - список для хранения найденных токенов
    tokens = []
    # current - для накопления числа (например, "2.5")
    current = ""
    # i - индекс текущего символа
    i = 0

    # Проходим по каждому символу в выражении
    while i < len(expr):
        char = expr[i]  # Текущий символ

        if char.isdigit() or char == '.':
            # Это цифра или точка - часть числа
            current += char
            i += 1  # Переходим к следующему символу

        elif char == '*' and i + 1 < len(expr) and expr[i + 1] == '*':
            # Нашли оператор возведения в степень **
            if current:
                tokens.append(current)  # Сохраняем накопленное число
                current = ""           # Очищаем накопитель
            tokens.append('**')        # Добавляем оператор **
            i += 2  # Пропускаем два символа (* и *)

        elif char in '+-*/%()':
            # Это оператор или скобка
            if current:
                tokens.append(current)  # Сохраняем накопленное число
                current = ""           # Очищаем накопитель
            tokens.append(char)        # Добавляем оператор
            i += 1  # Переходим к следующему символу

        elif char == ' ':
            # Пробел - разделитель токенов
            if current:
                tokens.append(current)  # Сохраняем накопленное число
                current = ""           # Очищаем накопитель
            i += 1  # Пропускаем пробел
        else:
            # Неизвестный символ - тоже добавляем как токен
            if current:
                tokens.append(current)
                current = ""
            tokens.append(char)
            i += 1

    # Не забываем сохранить последнее накопленное число
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
