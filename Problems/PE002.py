'''
Project Euler - Problem 2
https://projecteuler.net/problem=2

Author: F.C. Koorzen
GitHub: patchyPythonPirate

Here I wanted to create a method for finding the sum of Fibonacci numbers
between any start and end range, and able to specify if sum should include
only odd or even, or both.
Note: The following functions only work with positive integers!

Credit to Paul Hankin for a simple, efficient Fibonacci formula from
which all subsequent functions would not have been possible.
https://blog.paulhankin.net/fibonacci/
https://stackoverflow.com/a/37509291/10333604
'''
# Problem limit
limit = 4000000


# Thanks again Paul!
def fib(n):
    '''Returns the n-th fibonacci number'''
    return pow(2<<n,n+1,(4<<2*n)-(2<<n)-1)%(2<<n)


# The fibonacci numbers have a recurring pattern of even numbers;
# starting from index 0, every 3rd number is even; i.e. the index
# numbers which are all multiples of 3 are even fibonacci numbers,
# with the remainder being odd.
# Creating a standalone function is redundant; using a for
# loop, the range function with step 3, and fib(), one is able
# to produce the desired output. However, where the starting
# index is not 0, it is no longer as straight-forward.

def sumFibIndex(end,start=0,parity=None):
    '''
    Returns the sum of fibonacci numbers from start to end,
    'start' and 'end' is defined as the fib number index.
    By default, addition starts from index 0; fib(0)=0.
    
    Parity accepts string values 'odd' and 'even' as
    specification for addition. If None, everything is added.
    '''
    
    Sum = 0
    if parity == None:
        for i in range(start, end+1):
            Sum += fib(i)
            
    elif parity == 'odd':
        for i in range(start, end+1):
            if i % 3 != 0:
                Sum += fib(i)
                
    elif parity == 'even':
        for i in range(start, end+1):
            if i % 3 == 0:
                Sum += fib(i)
                
    else:
        raise Exception('parity must be set to "odd", "even" or None')
    
    return Sum
    

# This function checks its input against each fibonacci number
# with an infinite loop via a generator. It seems to work
# relatively efficiently, even for numbers as large as 10**2000.
# An algebraic method is still preferred, or atleast memoization,
# to reduce expense of iteration.

def findFibIndex(n):
    '''
    Returns a 2-tuple value where, if n is a fibonacci
    number, the first value as its index, and the second
    value as None.
    If n is not a fib number, the first value is the index
    of the largest fib number smaller than n, and the
    second value is the index of the smallest fib number
    larger than n.
    '''
    generator = fibGen()
    fibNum, i = generator.send(None)
    while n > fibNum:
        fibNum, i = generator.send(None)
        
    if fib(i) == n:
        return (i, None)
    else:
        return (i-1, i)


# Generator for fib sequence and index
def fibGen():
    '''Outputs a 2-tuple of a fibonacci number and its index, successively'''
    i = 0
    while True:
        yield fib(i), i
        i += 1


# Combine sumFib and fibIndex for a convenient function to sum
# fib numbers between range of integers, instead of per index

def sumFibRange(end,start=0,parity=None):
    '''
    Returns sum of fibonacci numbers between integer values
    for start and end
    '''
    # The starting value must either be fib, or use next fib in range
    if findFibIndex(start)[1] == None:
        b = findFibIndex(start)[0]
    else:
        b = findFibIndex(start)[1]
    # The end value must either be fib, or use the preceding fib in range
    e = findFibIndex(end)[0]

    return sumFibIndex(e, b, parity=parity)




# Solve for limit
if __name__ == "__main__":
    print(sumFibRange(limit, parity = 'even'))

