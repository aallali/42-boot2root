def func4(param):
    if (param <=1):
        return 1
    a = func4(param - 1)
    b = func4(param - 2)

    return a + b
   
i = 2
while i < 10:
    if (func4(i) == 55):
        print("yay " , i)
        quit()
    i += 1



