import math
a=float(input('Первое число:'))
b=float(input('Второе число:'))
c=input('Выберите действие:+,-,/,%:')
def calc(a,b,c):
    if c=='+':
        print(a+b)
    if c=='-':
        print(a-b)
    if c=='/':
        print(a/b)
    if c=='%':
        print(a%b)
calc(a,b,c)
