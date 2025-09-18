print("Привет пользователь, добро пожаловать в калькулятор")
result = 0
while True:
    try:
        if result == 0:
            num1 = float(input("Введите число 1: "))
        else:
            num1 = result
            print(f"Результат: {result}")


        operator = input("Введите оператор: ")

        if operator == "q":
            print("Пока")
            break
        elif operator == "c":
            result = 0
            print("Результат сброшен")
            continue

        num2 = float(input("Введите число 2: "))

        if operator == "+":
            result = num1 + num2
        elif operator == "-":
            result = num1 - num2
        elif operator == "/":
            result = num1 / num2
        elif operator == "*":
            result = num1 * num2

        print(f"Результат: {num1} {operator} {num2} = {result}")

    except Exception as e:
        print("Ошибка", e)