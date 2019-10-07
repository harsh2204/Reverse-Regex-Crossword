import re
import numpy as np
from typing import Tuple

from grid import setup_grid
import string

PatternVector = Tuple[str, str]


A = string.ascii_uppercase

puncs = string.punctuation

# pat = 'HE|LL|O+'
# pat = '[^SPEAK]+'


# random_words = open('accepted_words').read().split("\n")
# sel = random.choice(random_words)
# print("@"+sel+"@")
def check_pattern(pat):
    try :
        a = re.compile(pat)
        # print("regex compiled successfuly.")
        return True
    except:
        return False

def generate_pattern(l):
    print(l)
    letters = np.unique(l)
    print("letters")
    simple = "("+"|".join(letters) + ")+"
    print("simple regex: '" + simple + "' validity_test_pass: ", check_pattern(simple))
    # print(letters)

def pattern_amb(letter):
    return ".*"

class Pattern(object):
    def __init__(self, L):
        self.L = L
        self.type = ""
    
class PatternType(Pattern):
    def __init__(self, *args, **kwargs):
        pass

def pattern_range(letter):
    index = A.find(letter)
    low = np.random.randint(0,index+1)
    high = np.random.randint(index+1,len(A))
    return f'[{A[low]}-{A[high]}]'

def pattern_random_set(letter): # Fix duplicates
    max_range = 7
    pattern = np.array([letter])
    if np.random.uniform() < 0.10:
        max_range -= 1
        pattern = np.append(pattern, "\\"+np.random.choice(list(puncs)))
    Anp = np.array(list(A))
    Anp = np.delete(Anp, ord(letter)-65)
    np.random.shuffle(Anp)

    randoms =  Anp[0:np.random.randint(1, max_range+1)]
    pattern = np.append(pattern, randoms)
    np.random.shuffle(pattern)
    return f'[{"".join(list(pattern))}]'

def get_pattern(matrix: np.ndarray, ix: int, iy: int) -> PatternVector:
    # pass
    for x, y in np.ndindex(matrix.shape):
        col = matrix[:, y]
        row = matrix[x, :]
        intersect = row[np.in1d(row, col)]
        index = np.argwhere(intersect==matrix[x, y])
        intersect = np.delete(intersect, index)
        print(matrix[x, y], intersect)
    

matrix = setup_grid("Twelve Latte".upper())

print(matrix)

print("---Generating Patterns---")
# generate_pattern(matrix[:, 0])
col = matrix[:, 0]
row = matrix[0, :]

get_pattern(matrix, 0, 0)


print(pattern_random_set('T'))
"""
Progress on this file is on hold until the pattern module is completed. 
A lot of what is being done here is already in the pattern module. 
So this file will most likely be repurposed to a testing/example file.
"""