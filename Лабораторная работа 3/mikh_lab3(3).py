print("Задание 3, Вариант 7")
s=input("Введите строку:")
n=len(s)
count=s[:n//2].count("п")
s=s[:n//2].replace("п","*")+s[n//2:]
print(s)