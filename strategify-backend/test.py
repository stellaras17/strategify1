s = [0,0,0,0,0,0]
p = [0,0,0,0,0,0]
x =   [1, 4, 9, 8, 6] 


f = {
    1: 2,
    2: 6,
    3: 8,
    4: 9,
    5: 10,
    6: 10,
    7:10,
    8:10
}

for j in range(1,len(x)+1):
    s[j] = 0
    p[j] = 0
    for i in range(j):
        temp = s[i] + min(f[j-i], x[j-1])
        if (temp > s[j]):
            s[j] = temp
            p[j] = i 

print(s,p)
