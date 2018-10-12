'''
Project Euler - Problem 1
https://projecteuler.net/problem=1

Author: F.C. Koorzen
GitHub: patchyPythonPirate

The original challenge tasked participants to solve the puzzle with parameters 
X = 1000 and N = 3, 5 only. I wanted to create a function that could solve the 
puzzle for any value of X > 1, and any number of positive values N.

With the original parameters, the puzzle can be solved quickly enough with the 
Brute Force function from the Second Attempt. However, for values larger than 
10^12 the machine would spend upwards of 30 minutes calculating. Using the 
Algebraic method, with the same parameters, it is calculated in mere seconds.
'''
# Note: Main problems are handled first; imports and supporting functions
#       are created toward the end of the document.

################
# First Attempt
#
# Did not take into account that some values < X may be shared multiples of 
# numbers N, and therefore counted twice or more into Sum.
################

#                   Brute Force Method
#
# For multiples yielded by dividing integers from 1 to X(excluding)
# through numbers N, add each multiple to total Sum.

def sum_of_mult_bf(x, *n):
    '''Sum of multiples of N, for range of positive numbers less than X'''

    x, n = verify_and_clean_input(x, *n)

    Sum = 0
    for number in n:
        for integer in range(1,x):
            if integer % number == 0:  # check: is a multiple
                Sum += integer

    return Sum


#                       Algebraic Method
#
# Each number N produces a series of multiples of itself upto X
# Thus for each number N a Sum of series can be determined
# using the base formula of Sn = n/2[2a+(n-1)d]
# which can be reduced because a = d in this instance.
# Dividing X by N yields the number of possible multiples of N
# (as integers) within X. X itself is excluded from possible
# multiples, so we subtract 1 before doing the calculation.
# Repeat for each number N and add to total Sum.
#
# Note: The basic method of determining the number of multiples of
#       a single integer within a given range and the subsequent 
#       sum was outsourced to a generator for Attempt 2. Temptation
#       to replace the body of this function with the generator was
#       deferred to preserving the code for historical purposes.

def sum_of_mult_al(x, *n):
    '''Sum of multiples of N, for range of positive numbers less than X'''

    x, n = verify_and_clean_input(x, *n)

    Sum = 0
    for number in n:
        num_of_terms = (x-1)//number
        Sum += (number*num_of_terms*(num_of_terms+1))//2
        
    return Sum



#################
# Second Attempt
#
# Here we take into account that each integer leading up to X must only 
# be counted once.
#################

#                   Brute Force Method
#
# For each integer from 1 to X(excluding), check if divisible
# through N (check: is a multiple), and add integer to total Sum.
#
# Note: Here the loop order merely becomes switched opposed to Attempt One.
#       A break statement is added if the condition satisfies, to step to
#       the next integer value, that each integer may only be counted once.

def sum_of_mult_bf2(x, *n):
    '''Sum of multiples of N, for range of positive numbers less than X'''

    x, n = verify_and_clean_input(x, *n)
    
    Sum = 0
    for integer in range(1,x):
        for number in n:
            if integer % number == 0:
                Sum += integer
                break

    return Sum


#                       Algebraic Method
#
# Using algebraic methods, the puzzle revealed a pattern whereby the Total
# Sum is calculated by adding the sum of the product of each unique 
# combination(s) of N; but where such a combination size is even numbered,
# it must be multiplied by negative one. This can be demonstrated as:
#
# where f(n) is the sum of all the multiples of n within a given range, and
# where a,b,c is the given number n, then
#
# Total Sum = f(a) + f(b) + f(c) - f(ab) - f(ac) - f(bc) + f(abc)
#

def sum_of_mult_al2(x, *n):
    '''Sum of multiples of N, for range of positive numbers less than X'''

    x, n = verify_and_clean_input(x, *n)

    # Setup generator
    func = sum_generator(base=x)  # Set base range
    f = func.send                 # Name send/yield method
    f(None)                       # Activate generator

    Sum = 0
    for size in range(1, len(n)+1):
        # If size odd, add series sum
        if size % 2 != 0:
            for combo in combine(n, size):
                Sum += f(product(combo))
        # If size even, subtract series sum
        if size % 2 == 0:           
            for combo in combine(n, size):
                Sum -= f(product(combo))
                
    return Sum

#########################
# Supporting Functions
#########################

# import unique combinator
# returns an iterator that outputs unique combination tuples of 
# specified length
from itertools import combinations as combine

def product(iterobj):
    '''Returns the product of all items in an iterable object.'''
    product = 1
    for i in iterobj:
        product = product * i
    return product


def sum_generator(base=None, result=None):
    '''Yields the sum of multiples for given number within range Base'''
    while True:
        number = yield result
        quotient = (base-1)//number
        result = number*quotient*(quotient+1)//2

# import verification functions
# This is included for completeness only; this import and its dependant
# function can be removed without ill effect.
from screening import isNumber, GreaterThan, uniqMembers
        
def verify_and_clean_input(x, *n):
    '''Screening function'''    
    isNumber(x)
    isNumber(*n)         # Don't forget to unpack tuple values!
    GreaterThan(1, x)    # Verify x is greater than 1
    GreaterThan(1, *n)   # Verify n members are greater than 1
    
    n = uniqMembers(*n)  # return non-multiple, unique values for n
            
    return x, n
