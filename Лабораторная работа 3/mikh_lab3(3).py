print("Задание 3, Вариант 7")
ok = False
while not ok:
    s = input("Введите строку: ")
    if len(s)==0:
        print("Ошибка! Строка не должна быть пустой.")
    else:
        ok = True

n = len(s)
s = s[:n // 2].replace("п", "*") + s[n // 2:]
print(s)