# import tkinter
import sys
print("Hello World!")
a=sys.path
for i in a:
    print(i)
A=[2,4,6,8,10]

for i,a in enumerate(A):
    if a%10 : A[i]=a%10
    if a == 2: A[i]='two'
print(A)
