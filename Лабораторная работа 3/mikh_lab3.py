print("Задание 1, Вариант 7")
ok = False
while not ok:
    try:
        number_list = [int(x) for x in input("Введите целые числа через пробел (последовательность оканчивается нулем): ").split()]
        if len(number_list) == 0:
            print("Ошибка! Последовательность не должна быть пустой. Введите числа через пробел.")
        elif number_list[-1] != 0:
            print("Ошибка! Последний элемент последовательности должен быть нулем.")
        else:
            ok = True
    except ValueError:
        print("Ошибка! Вводите только целые числа через пробел.")

sum = 0
count = 0
for x in number_list:
    sum += x
    count += 1
print("Сумма чисел последовательности:", sum)
print("Количество элементов последовательности:", count)