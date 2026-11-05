print("Задание 5, Вариант 7")
n=list(map(int,input("Введите массив целых чисел:").split()))
max=max(n)
min=min(n)
max_ind=n.index(max)
min_ind=n.index(min)
n[max_ind]= min
n[min_ind]=max
print("Преобразованный массив:", n)