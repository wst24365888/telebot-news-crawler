from fractions import Fraction
#from math import gcd

deg = 0
result = 0
terms = []

def gcd(x,y):

    if x%y == 0:
        return y

    return gcd(y,x%y)

def calculate(root):

    global terms

    sum = 0

    for i in range(deg+1):
        sum += terms[i]*root**i

    return sum

def check(denominator, numerator):

    reply = ''

    global result

    if calculate(Fraction(numerator, denominator)) == 0:
        if denominator==1:
            reply += "(x+{})".format(numerator)
        else:
            reply += "({}x+{})".format(denominator,numerator)
        result += 1

    if calculate(Fraction(numerator, denominator)*(-1)) == 0:
        if denominator==1:
            reply += "(x-{})".format(numerator)
        else:
            reply += "({}x-{})".format(denominator,numerator)
        result += 1
    
    return reply

def main():

    input_terms = input('Please input the terms of each degree, and saperate by commmas => ')
    terms_temp = input_terms.split(',')

    global deg
    deg = len(terms_temp)-1    #次數

    global result
    result = 0

    global terms
    terms = [int(term) for term in terms_temp][::-1]    #[::-1]->Reverse

    reply = ""

    terms_constant = abs(terms[0])
    terms_highest = abs(terms[deg])

    for i in range (1,terms_highest+1):
        if terms_highest%i == 0:
            for j in range (1,terms_constant+1):
                if terms_constant%j == 0:
                    if gcd(i,j) == 1:
                        reply += check(i,j)

    if result == 0:
        reply += 'Sorry, there is no result.'

    return reply

if __name__ == "__main__":
    print(main())