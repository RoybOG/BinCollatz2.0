from Utils import *

"""
All the checks require 0 multiplication, just bit manipulation
"""




def alg(n):
    #Making sure the tests later will be on odd number. 
    # if first digit is 0 then remove trailing zero
    # otherwise if second digit is 1 than its a trailing 1s if its 0, than it can be alt or a gate. we can check by the countgate zeros if its more than 1.
    
    # Two points for improvment:
    # 1. The power and multiplication by the number are the biggest bottlenecks 
        # Try to minimize the number of powers needed to be calculated or have them the same 
    # 2. I calculate using big powers only to divide after, there must be a cleaner way to calculate it, to raise and dievide at the same step!

    c = countGateLength(n) #count how many zeros after the first digit of 1

    if (c == 0): 
        #if the second digit is one
        #it means the number is starting with a string of 1s.
        c = countTrailingOnes(n) 
        n = 3**c * (n + 1)-2**c


    elif c == 1:
            
            #Than its starts with a string of alternating digits
            #c = countAltLenth(n)
            n = 3*n + 1 
    else:
        shiftedC = c>>1
        n = 3**(1+shiftedC)*(n-1)+2**((shiftedC<<1)+2)
        #its a gate string



    #if not (n  & 1): #check if even
            #n = stripTrailingZeros(n) 
    
    return stripTrailingZeros(n) 



def steriodsCollaz(n):
    steps = 1
    print(n)
    while n > 5:
        n = alg(n)
        steps= steps + 1
        #print(n)
    print(f'done in {steps} steps')



if __name__ == '__main__':
    steriodsCollaz(int(input("Enter a number: "),0))
