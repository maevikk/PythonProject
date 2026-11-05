print("Задание 2, Вариант 7")
ok = False
while not ok:
    try:
        n = int(input("Введите целое число N > 1: "))
        if n > 1:
            ok = True
        else:
            print("Ошибка! Число должно быть больше 1.")
    except ValueError:
        print("Ошибка! Нужно ввести целое число, например 10.")

k = 0
while 2 ** k <= n:
    k += 1
print("k =", k)