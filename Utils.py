import time
from functools import wraps


toBitStr = lambda b: format(b, 'b')

# ------decorators--------
def time_performance(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()  # Start high-res timer
        result = func(*args, **kwargs)
        end_time = time.perf_counter()    # End timer
        
        duration = end_time - start_time
        print(f"[{func.__name__}] Executed in {duration:.6f} seconds")
        return result
    return wrapper






def binStrFunc(func):
    def wrapper(*args, **kwargs):
        altArgs = list(args)
        
        altArgs[0] = int(args[0],0) if type(altArgs[0]) is str else args[0]
        result = func(*altArgs, **kwargs)
        if result is not None:
            print(toBitStr(result))
        return result
    return wrapper


def is_binary(s):
    # מחזיר True רק אם המחרוזת לא ריקה וכוללת רק 0 ו-1
    return set(s).issubset({'0', '1'})



def countTrailingZeros(n):
    return (n & -n).bit_length() - 1 #Try to remove the -1, costly than a logic gate

def stripTrailingZeros(n):
    #the negative is 2's complement: inverting all the bits and adding 1. 
    #the trailing zeros will invert to 1 and adding 1 will bring them back to 0. 
    #however, the left bits will still be left inverted, thus ANDing them will cancel them, leaving the single one.
    return n >> countTrailingZeros(n)


def countTrailingOnes(n):
    return countTrailingZeros(~n) 


def countGateLength(n):
    #if a number is ...011...1111 + 1 = ...100...000000000
    # the sequence of ones will be ended with a zero digit, which will become one after we add 1 to all the zeros.
    
    
    return countTrailingZeros(n >> 1)

def countAltLenth(n):
    # 1. Xors the number with a left shifter version of itself. c
    # As log as nighbouring digits are different it will be one
    return countTrailingOnes(n ^ (n << 1))


def isGrowing(n):
    return countTrailingOnes(n)>1