
x=3*16**20+81*16**12-9*16**3
w=''
while x!=0:
    w+=str(x%5)
    x//5
print(w.count(max(w)))