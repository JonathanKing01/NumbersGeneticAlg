import random
import sys

#Initialize library of encoded values:
numbers = dict([('0000',0), ('0001',1),('0010',2),('0011',3),('0100',4),('0101',5),('0110',6),('0111',7),('1000',8),('1001' ,9)]);

goal = 0
crossRate = 0.7
mutationRate = 0.01

def genPop(size, length):
    pop = []
    for i in range(size):
        g = ''
        for i in range(length*4):
            g += str(random.getrandbits(1))
        pop += [g]
    return pop

#Function for decoding strings of bits
def decode (s):
    bit = ''
    out = ' '
    i = 0
    while i < len(s):
        bit = str(s[i:i+4])
        if bit == '1010' and out[-1] not in '+-*/ ':
            out += '+'
        elif bit == "1011" and out[-1] not in '+-*/ ':
            out += '-'
        elif bit == "1100" and out[-1] not in '+-*/ ':
            out += '*'
        elif bit == "1101" and out[-1] not in '+-*/ ':
            out += '/'
        elif out[-1] in '+-*/ ':
            try:
                out += str(numbers[bit])
            except KeyError:
                out = out
        i+=4
    if out[-1] in '+-*/ ':
        out = out[:-1]
    return out[1:]

def fitness (g,target):
    try:
        return 1/(abs(target-eval(decode(g))))
    except ZeroDivisionError:
        try:
            eval(decode(g))
            print('Answer found: ' + decode(g))
            sys.exit(0)
        except ZeroDivisionError:
            return 0

def makeRW(pop,target):
    total = 0
    wheel = [0]
    for x in pop:
        total += fitness(x,target)
    deg = 360/total
    for x in pop:
        wheel += [wheel[-1] + deg*fitness(x,target)]
    return wheel

def RWselection(wheel):
    pick = random.randrange(0,360)
    i = 0
    while wheel[i]-pick< 0:
        i += 1
    return i

def pick2 (pop, wheel):
    a = pop[RWselection(wheel)-1]
    b = pop[RWselection(wheel)-1]
    # Crossover checking
    if random.randrange(0,100)/100 < crossRate:
        pivot = random.randrange(len(a))
        temp = a[pivot:]
        a = a[:pivot] + b[pivot:]
        b = b[:pivot] + a[pivot:]
    # Mutation checking
    for x in a:
        if random.randrange(0,100)/100 <= mutationRate:
            if x == 0:
                x = 1
            else:
                x = 0
    for x in b:
        if random.randrange(0,100)/100 <= mutationRate:
            if x == 0:
                x = 1
            else:
                x = 0
    return [a,b]

def genNewPop(oldPop,target):
    newPop = []
    wheel = makeRW(oldPop,target)
    for i in range(int(len(oldPop)/2)):
        newPop += pick2(oldPop,wheel)
    return newPop


def solve(size, length, it,target):
    pop = genPop(size,length)
    for i in range(it):
        pop = genNewPop(pop,target)
    print("Solution not found after " + str(it) + " iterations")
    return


print("Enter a number to compute a formula for. ")
target = int(input())
print("Enter a population size")
size = int(input())
print("Enter a starting formula length")
length = int(input())
print("Enter a number of iterations")
it = int(input())
print("Computing now.")
solve(size, length,it,target)
