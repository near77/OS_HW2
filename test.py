

a = [1, 2, 4, 5, 7]

b = []

for i in range(10):
    flag = 0
    for A in a:
        if i == A:
            flag = 1
    if flag == 0:
        b.append(i)

print(b)