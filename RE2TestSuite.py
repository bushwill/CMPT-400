from FAdo.reex import *
from FAdo.conversions import *
from FAdo.fa import *

def genRegExp(reg):
    if len(reg) == 1:
        return reg
    i = 0
    current_reg = []
    while i < len(reg):
        if reg[i] == "(":
            rightBracketIndex = findMatchingRightBracket(reg, i)
            current_reg.append(genRegExp(reg[i+1:rightBracketIndex]))
            i=rightBracketIndex+1
        elif reg[i].isalpha():
            current_reg.append(reg[i])
            i+=1
        elif reg[i] == "*" or reg[i] == "+":
            current_reg.append(reg[i])
            i+=1
    return current_reg
            
def findMatchingRightBracket(reg, leftBracketIndex):
    leftBrackets = 1
    i = leftBracketIndex
    while leftBrackets > 0:
        i+=1
        if reg[i] == "(":
            leftBrackets+=1
        elif reg[i] == ")":
            leftBrackets-=1
    return i

reg = str2regexp("(a+b)*")
print(genRegExp("aabb(a(bab)a)*"))
print(reg.toDFA())
