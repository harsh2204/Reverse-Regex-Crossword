import re
import numpy as np

from grid import setup_grid
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



matrix = setup_grid("TwelveLetter".upper())

print(matrix)

print("---Generating Patterns---")
generate_pattern(matrix[:, 0])
