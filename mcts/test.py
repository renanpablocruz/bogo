def plus(a, b):
    return a + b

def minus(a, b):
    return a - b

handlers = {
            'plus' : plus,
            'minus' : minus
            }

f = handlers['plus']
print f(1,2)