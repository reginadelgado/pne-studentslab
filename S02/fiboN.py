def fibon(n):
    n1 = 0
    n2 = 1

    for i in range(n):
        n3 = n1 + n2
        n1 = n2
        n2 = n3

    nth_term = n1
    print(str(n) + "th Fibonacci term is: " + str(nth_term) + ".")

fibon(5)
fibon(10)
fibon(15)

