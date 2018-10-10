'''
Project Euler - Problem 1
https://projecteuler.net/problem=1

Author: C. Koorzen
GitHub: PatchyPythonPirate

The original challenge tasked participants to solve the puzzle with parameters 
X = 1000 and N = 3,5 only. I wanted to create a function that could solve the 
puzzle for any value of X > 1, and any number of multiples N.

With the original parameters, the puzzle can be solved quickly enough with the 
Brute Force function in the Second Attempt. However, for values larger than 
10^12 the machine would spend upwards of 30 minutes calculating. Using the 
Algebraic method, with the same parameters, it is calculated in mere seconds.
'''


################
# First Attempt
#
# Did not take into account that some values < X may be shared multiples of 
# N, and therefore counted twice or more into Sum
################

#                   Brute Force Method
#
# For integers yielded by dividing numbers from 1 to X(excluding)
# through multiple N, add each integer to total Sum.

def sum_of_mult_bf(x, *n):
    '''Sum of multiples of N, for range of positive numbers less than X'''

    x, n = verify_and_clean_input(x, *n)

    Sum = 0
    for multiple in n:
        for number in range(1,x):
            if number % multiple == 0:
                Sum += number

    return Sum


#                       Algebraic Method
#
# Each multiple N produces a series of multiples of itself upto X
# Thus for each multiple a Sum of series can be determined
# using the base formula of Sn = n/2[2a+(n-1)d]
# which can be reduced because a = d in this instance.
# Dividing X by N yields the NUMber of possible multiples of N
# (as integers) within X. X itself is excluded from possible
# multiples, so we subtract 1 before doing the calculation.
# Repeat for each multiple N and add to total Sum.
#
# Note: The basic method of determining the number of multiples of
#       a single integer within a given range and the subsequent 
#       sum was outsourced to the generator in Attempt 2. Temptation
#       to replace the body of this function with the generator was
#       deferred to preserving the code for historical purposes.

def sum_of_mult_al(x, *n):
    '''Sum of multiples of N, for range of positive numbers less than X'''

    x, n = verify_and_clean_input(x, *n)

    Sum = 0
    for multiple in n:
        num_of_terms = (x-1)//multiple
        Sum += (multiple*num_of_terms*(num_of_terms+1))//2
        
    return Sum



#################
# Second Attempt
#
# Here we take into account that each integer leading up to X must only 
# be counted once.
#################

#                   Brute Force Method
#
# For each number from 1 to X(excluding), check if divisible
# through multiple N, and add integer to total Sum.
#
# Note: Here the loop order merely becomes switched opposed to Attempt One

def sum_of_mult_bf2(x, *n):
    '''Sum of multiples of N, for range of positive numbers less than X'''

    x, n = verify_and_clean_input(x, *n)
    
    Sum = 0
    for number in range(1,x):
        for multiple in n:
            if number % multiple == 0:
                Sum += number
                break

    return Sum


#                       Algebraic Method
#
# Using algebraic methods, the puzzle revealed a pattern whereby the Total
# Sum is calculated by adding the sums of each unique combination of the
# possible Multiples together, but multiplying each even combination by
# negative one. This can be demonstrated as:
#
# where f(n) is the sum of all the multiples of n within a given range, and
# where a,b,c is the given multiples, then
#
# Total Sum = f(a) + f(b) + f(c) - f(ab) - f(ac) - f(bc) + f(abc)

def sum_of_mult_al2(x, *n):
    '''Sum of multiples of N, for range of positive numbers less than X'''

    x, n = verify_and_clean_input(x, *n)

    # Setup generator
    func = sum_generator(base=x)
    f = func.send
    f(None)

    Sum = 0
    for pos in range(len(n)):
        number = pos + 1
        if number % 2 != 0:
            for mult in combine(n, number):
                Sum += f(product(mult))
        if number % 2 == 0:
            for mult in combine(n, number):
                Sum += (f(product(mult)))*-1
                
    return Sum

#########################
# Supporting Functions
#########################

# import unique combinator
# returns an iterator that outputs integer tuples of specified length
from itertools import combinations as combine

def product(iterobj):
    '''Returns the product of all items in an iterable object.'''
    product = 1
    for i in iterobj:
        product = product * i
    return product


def sum_generator(base=None, result=None):
    '''Generates the sum of multiples for all integers less than Base'''
    while True:
        multiple = yield result
        quot = (base-1)//multiple
        result = multiple*quot*(quot+1)//2

# import verification functions
from screening import isNumber, GreaterThan, uniqMembers
        
def verify_and_clean_input(x, *n):
    '''Screening function'''    
    isNumber(x)
    isNumber(n)
    GreaterThan(1, x)   # Verify x is greater than 1
    GreaterThan(1, n)   # Verify n members is greater than 1
    
    n = uniqMembers(n)  # return non-multiple unique values for n
            
    return x, n
