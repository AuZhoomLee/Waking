def format_Matrix(diff):
    replenish=[0 for i in range(diff)]
    return replenish
    pass

print(format_Matrix(5))

a=[[1,3,4,5],[2,3,4,6]]
b=[[1,3,4],[2,3,4]]

for i in b:
    b+=format_Matrix(len(a[0])-len(b[0]))
    pass

print(a,b)
