def fibosum(n):
    n1 = 0
    n2 = 1
    sum = 0
    for i in range(n):
        n3 = n1 + n2
        n1 = n2
        n2 = n3
        sum += n1

    print("The sum of the first " + str(n) + "terms of the Fibonacci series is: " + str(sum))

fibosum(5)
fibosum(10)
