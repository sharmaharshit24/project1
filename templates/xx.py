def nCr(n, r): 
  
    return (fact(n) / (fact(r)  
                * fact(n - r))) 



t = int(input())
for _ in range(t):
    n = int(input())
    a = list(input())
    b = list(input())
    
    a1 = 0
    a0 = 0
    for i in a:
        if i == '1':
            a1 += 1
        else:
            a0 += 1
    b1 = 0
    b0 = 0
    l = []
    for i in b:
        if i == '1':
            b1 += 1
        else:
            b0 += 1
    max1 = 0
    maxd = 0
    mind = 0
    # max1 = min(n, b1 + a1)
    if b1 + a1 > n:
        max1 = n - a1 + n - b1
        maxd = n - max1
    else:
        maxd = 0
        max1 = a1 + b1
    
    min1 = abs(b1-a1)
    mind = min(b1, a1)
    d = maxd
    ans = 0
    mod = 1000000007
    i = min1
    while i <= max1:
        l.append(i)
        ans = (ans + nCr(n, i))%mod
        if d < mind:
            d += 1
            i += 2
        else:
            i += 1
    # print(*a)
    # print(*b)
    print(int(ans))
    # print(l)
    # print()
    