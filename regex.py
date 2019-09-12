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
    pass

def pattern_range(letter):
    index = A.find(letter)
    low = np.random.randint(0,index+1)
    high = np.random.randint(index+1,len(A))
    return f'[{A[low]}-{A[high]}]'

def pattern_random_set(letter): # Fix duplicates
    max_range = 7
    pattern = np.array([letter])
    if np.random.uniform() < 0.50:
        max_range -= 1
        np.append(pattern, "\\"+np.random.choice(list(puncs)))
    Anp = np.array(list(A))

    randoms = np.random.choice(Anp[Anp!=letter], np.random.randint(1, max_range+1))
    
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
    


# Regex all possible rules:
#   Pattern | String
#    abcd   |  abc
#   a(b|c)d |  abd & acd
#  (ab)|(cd)|  ab & cd
#    [abc]  |  abc
#           |
#           |
#           |
#           |
#           |
#           |
#           |
#           |
#           |
#           |
# 
# How should I do this? Letter by letter, and use the information of the 
# two words to generate two different patterns for the same letter on 
# two different words   

# BASIC: (SAUCE: https://cs.lmu.edu/~ray/notes/regex/)
# hello	                contains {hello}
# gray|grey	            contains {gray, grey}
# gr(a|e)y	            contains {gray, grey}
# gr[ae]y	            contains {gray, grey}
# b[aeiou]bble	        contains {babble, bebble, bibble, bobble, bubble}
# [b-chm-pP]at|ot	    contains {bat, cat, hat, mat, nat, oat, pat, Pat, ot}
# colou?r	            contains {color, colour}
# rege(x(es)?|xps?)	    contains {regex, regexes, regexp, regexps}
# go*gle	            contains {ggle, gogle, google, gooogle, goooogle, ...}
# go+gle	            contains {gogle, google, gooogle, goooogle, ...}
# g(oog)+le	            contains {google, googoogle, googoogoogle, googoogoogoogle, ...}
# z{3}	                contains {zzz}
# z{3,6}	            contains {zzz, zzzz, zzzzz, zzzzzz}
# z{3,}	                contains {zzz, zzzz, zzzzz, ...}
# [Bb]rainf\*\*k	    contains {Brainf**k, brainf**k}
# \d	                contains {0,1,2,3,4,5,6,7,8,9}
# \d{5}(-\d{4})?	    contains a United States zip code
# 1\d{10}	            contains an 11-digit string starting with a 1
# [2-9]|[12]\d|3[0-6]	contains an integer in the range 2..36 inclusive
# Hello\nworld	        contains Hello followed by a newline followed by world
# mi.....ft	            contains a nine-character (sub)string beginning with mi and ending with ft (Note: depending on context, the dot stands either for “any character at all” or “any character except a newline”.) Each dot is allowed to match a different character, so both microsoft and minecraft will match.
# \d+(\.\d\d)?	        contains a positive integer or a floating point number with exactly two characters after the decimal point.
# [^i*&2@]	            contains any character other than an i, asterisk, ampersand, 2, or at-sign.
# //[^\r\n]*[\r\n]	    contains a Java or C# slash-slash comment
# ^dog	                begins with "dog"
# dog$	                ends with "dog"
# ^dog$	                is exactly "dog"




matrix = setup_grid("Twelve Latte".upper())

print(matrix)

print("---Generating Patterns---")
# generate_pattern(matrix[:, 0])
col = matrix[:, 0]
row = matrix[0, :]

get_pattern(matrix, 0, 0)