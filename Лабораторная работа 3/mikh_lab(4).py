print("Задание 4, Вариант 7")
ok = False
while not ok:
    try:
        m = list(map(int, input("Введите целые числа через пробел: ").split()))
        if len(m) == 0:
            print("Ошибка! Массив не должен быть пустым.")
        else:
            ok = True
    except ValueError:
        print("Ошибка! Вводите только целые числа через пробел.")

s = 0
p = 1
for i in range(len(m)):
    if (i + 1) % 2 == 0:
        s += m[i]
    else:
        p *= m[i]
print("Сумма элементов:", s)
print("Произведение элементов:", p)