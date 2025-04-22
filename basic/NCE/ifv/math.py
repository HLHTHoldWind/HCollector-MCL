"""The ifv's math moudle"""

from .ifv import *
from fractions import Fraction

def abs(num):
    """Abs a number"""
    if num<0:
        num = num*-1
    else:
        num = num
    return num

def float_e(num):
    """I don't care any numbers"""
    if type(num)==type('a'):
        if num==('-'):
            final = (-1.0)
        elif num.startswith('-'):
            num = num.lstrip('-')
            final = float(num)
            final = -1.0*final
        else:
            final = float(num)
    else:
        final = float(num)
    return final

def average(nums):
    """Return the nums' average"""
    nums = list(nums)
    final = 0
    for i in nums:
        final+=i
    final = final/len(nums)
    return final
mean = average

def weighted_mean(nums, weights):
    """Calc the weighted mean"""
    nums = list(nums)
    weights = list(weights)
    mother = 0
    for i in weights:
        mother+=i
    final = 0
    times = 0
    for i in nums:
        final+=i*weights[times]
    final = final/mother
    return final
weightedMean = weighted_mean
weightedAverage = weighted_mean
w_mean = weighted_mean

def variance(nums):
    """Return the nums' variance"""
    nums = list(nums)
    aver = average(nums)
    total = 0
    for i in nums:
        total+=(i-aver)**2
    final = total/len(nums)
    return final

def standard_deviation(nums):
    """Return the nums' standard deviation"""
    return variance(nums)**0.5
stdev = standard_deviation

def isEvenNumber(num):
    return True if num%2==0 else False

def median(nums):
    """Return the nums' median"""
    nums = list(nums)
    nums.sort()
    if isEvenNumber(len(nums)):
        return average((nums[int(len(nums)/2)-1],nums[int(len(nums)/2)]))
    else:
        return nums[int(len(nums)/2)]

def mode(nums):
    """Return the nums' mode"""
    nums = list(nums)
    total = {}
    for i in nums:
        if i not in total:
            total[i] = 0
        else:
            total[i]+=1
    final = 0
    finals = []
    for i in total:
        try:
            if total[i]>total[final]:
                final = i
            elif total[i]<total[final]:
                pass
            elif total[i]==total[final] and finals==[]:
                finals.append(final)
                finals.append(i)
            else:
                finals.append(i)
        except:
            final = i
    if finals==[]:
        return final
    elif len(finals)==len(nums):
        return None
    else:
        return tuple(finals)

def round_e(num, width):
    """Round num into width"""
    num_list = list(str(num))
    time = 0
    for i in num_list:
        if i == '.':
            break
        time+=1
    lenth = time+width+2
    if len(num_list)<lenth and '.' not in num_list:
        raise TypeError(''+
                        'Invalid parameter: "'+
                        str(num)+'" must be a float not an integer or a string.')
    if len(num_list)<lenth and '.' in num_list:
        while len(num_list)<lenth:
            num_list.append('0')
    while len(num_list)!=lenth:
        del num_list[-1]
    if int(num_list[-1])>=5:
        del num_list[-1]
        num_list[-1]=str(int(num_list[-1])+1)
    else:
        del num_list[-1]
    final=''
    for i in num_list:
        final+=i
    final = float(final)
    return final

def randfloat(num1, num2, width=2):
    """Return random float in range [num1, num2]."""
    if width>15:
        raise LengthError(''+
                          'Parameter too large: '
                          'width"'+str(width)+'"is larger than 15.')
    r = random
    a = r.randint(num1, num2-1)
    b = r.random()
    c = a+b
    c = round_e(c, width)
    return c

def getLinearFunction(point1, point2, numbers=False):
    """point1 (tuple), point2(tuple)"""
    x1 = point1[0]
    x2 = point2[0]
    y1 = point1[1]
    y2 = point2[1]
    k = Fraction((y1-y2), (x1-x2))
    b = Fraction(float(y1-(k*x1)))
    if numbers:
        final = (k, b)
    else:
        if k==1:
            k = ''
        if b!=0:
            if b>=0:
                final = f"y={k}x+{b}"
            else:
                final = f"y={k}x-{b}"
        else:
            final = f"y={k}x"
    return final
getLF = getLinearFunction

def returnLFkb(function):
    temp = function
    bF = False
    while not temp.endswith('/'):
        temp = temp[:-1]
        if temp=='':
            break
    if 'x' not in temp:
        temp = function
    i = ''
    while i!=' ' and i!='+' and i!='-':
        temp = temp[:-1]
        if temp=='':
            break
        i = temp[-1]
    k = temp.rstrip('x +-')
    k = k.lstrip('y =')
    if k=='':
        k = 1
    temp = function
    while not temp.startswith('/'):
        temp = temp[1:]
        if temp=='':
            break
    if 'x' not in temp:
        temp = function
    i = ''
    while i!=' ' and i!='+' and i!='-':
        temp = temp[1:]
        if temp=='':
            break
        i = temp[0]
    b = temp.lstrip('+ ')
    if temp.startswith('-'):
        bF = True
    else:
        bF = False
    i = ''
    if bF:
        b = b[1:]
        while i!=' ' and i!='+' and i!='-':
            b = b[1:]
            i = b[0]
        b = Fraction(b)
    if b=='':
        b = 0
    k = Fraction(k)
    b = Fraction(b)
    return k, b

def euclideanDistance(point1, point2):
    """point1 (tuple), point2(tuple)"""
    x1 = point1[0]
    x2 = point2[0]
    y1 = point1[1]
    y2 = point2[1]
    final = Fraction((((x1-x2)**2)+((y1-y2)**2))**0.5)
    return final
getDis = euclideanDistance

def pointToLinearFunction(point, function):
    """point (tuple), function(str)"""
    x1, y1 = point
    k2, b2 = returnLFkb(function)
    k1 = Fraction((k2*-1)**-1)
    b1 = Fraction(y1-(k1*x1))
    x2 = Fraction(b1-b2,k2-k1)
    y2 = Fraction((k2*x2)+b2)
    distance = getDis((x1,y1), (x2,y2))
    return distance
ptfDis = pointToLinearFunction

def radical(data):
    """Turn a data to the radical type"""
    square = round(float(data**2),15)
    final = f"√{square}"
    return final