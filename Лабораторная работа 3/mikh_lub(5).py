print("Задание 5, Вариант 7")
ok = False
while not ok:
    try:
        n = list(map(int, input("Введите массив целых чисел через пробел: ").split()))
        if len(n) == 0:
            print("Ошибка! Массив не должен быть пустым.")
        else:
            ok = True
    except ValueError:
        print("Ошибка! Вводите только целые числа через пробел.")

max = max(n)
min = min(n)
max_ind = n.index(max)
min_ind = n.index(min)
n[max_ind] = min
n[min_ind] = max
print("Преобразованный массив:", n)