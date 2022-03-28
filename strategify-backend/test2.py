w= 3
x = [2, 3, 0, 1, 4, 4, 1, 0, 4, 0, 1, 6, 4]
s = [min(w*w,x[0]),0,0,0,0,0,0,0,0,0,0,0,0,0,0]
p = [min(w*w,x[0]),0,0,0,0,0,0,0,0,0,0,0,0,0,0]

for j in range(1,len(x)+1):
    s[j] = 0
    p[j] = 0
    for i in range(0,j,2):
        temp = s[i] + min(w*w, x[j-1])
        if (temp > s[j]):
            s[j] = temp
            p[j] = i
print(s,p)
