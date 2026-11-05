print("Задание 4, Вариант 7")
m=list(map(int,input("Введите элементы массива через пробел:").split()))
s=0
p=1
for i in range(len(m)):
    if (i+1)%2==0:
        s+=m[i]
    else: p*=m[i]
print("Сумма элементов:", s)
print("Произведение элементов:", p)