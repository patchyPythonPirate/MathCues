'''
A module containing variable verification functions.
'''

# Integers
# Validation through Exception

def isNumber(*n):
    '''Checks if n is a number'''
    for item in n:
        if type(item) != type(int()) and type(item) != type(float()):
            raise Exception('Variable must either be integer or float')

def GreaterThan(x, *n):
    '''Checks if n is greater than x'''
    for item in n:
        if not item > x:
            raise Exception('Variable must be greater than {0}'.format(x))
            
def LessThan(x, *n):
    '''Checks if n is less than x'''
    for item in n:
        if not item < x:
            raise Exception('Variable must be less than {0}'.format(x))


# Cleanup functions

def uniqValues(*n):
    '''Returns a tuple with unique values'''
    return tuple(set(n))
    
def noMultiple(*n):
    '''Returns a tuple where member values are not multiples of each other'''
    members = list(n)
    members.sort()
    multiples = list()
    for denominator in members:
        for numerator in members:
            if numerator == denominator:
                continue
            if numerator % denominator == 0:
                multiples.append(numerator)
                
    for item in set(multiples):
        members.remove(item)
        
    return tuple(members)
