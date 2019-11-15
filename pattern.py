import numpy as np
from random import randrange, sample
import string
from pprint import pprint

class PatternBase(object):

    negatable = False

    def __init__(self, pattern, *args, **kwargs):
        self.v = pattern.v
        self.N = self.v.size
        self.is_un = pattern.is_un
        self.uni_steps = pattern.uni_steps
        self.U = pattern.U
        self.chopped = pattern.chopped

class SimplePattern(PatternBase):
    def make_pattern(self):      
        if not self.is_un:
            self.chopped = ["".join(x) for x in self.chopped]
        return self.chopped

class SimpleORS(PatternBase):
    def make_pattern(self):
        # we will make a random or dup and concatenate it as, rand|letter. 
        
        # TODO: Implement partial randomness rather than full randomness
        patterns = []  

        for l in self.chopped:
            random_set = np.array(list(self.U))         
            np.random.shuffle(random_set)
            random_set = np.delete(random_set, [self.U.index(letter) for letter in l])
            random_set = random_set[:len(l)]
            random_string = "".join(list(random_set))
            # if l == random_string:
            #     random_string = self.U[(self.U.index(l[0]) + 1)] + l[1:] if self.U.index(l[0]) + 1 < len(self.U) else self.U[0] + l[1:]

            p = f'({random_string}|{"".join(l)})' if np.random.uniform() < 0.50 else f'({"".join(l)}|{random_string})'
            patterns.append(p)
        return patterns

class ORS(PatternBase):

    def make_ors(self, l: str, max_randoms=3):
        # make a random set of N terms where l is appended, and the set is shuffled. 
        # alternatively we could use a random index to append to the set which would bring down the iterations.
        # Note: we must make sure that we don't have l in our randomly selected set of N terms.
        
        # print(l)
        pattern = np.array(l)
        N = randrange(1, max_randoms)
        
        star = "" if len(l) == 1 and np.random.uniform() < 0.50 else "*"
        if len(l) != 1 and (np.random.uniform() < 0.50):
            star = "+"
            
        random_set = np.array(list(self.U))
        random_set = np.delete(random_set, [self.U.index(letter) for letter in l])
        np.random.shuffle(random_set)
        random_set = random_set[:N]

        pattern = np.append(pattern, random_set)
        np.random.shuffle(pattern)
        return f"({'|'.join(list(pattern))}){star}"

        
    def make_pattern(self):
        if self.N < 3:
            return "".join(list(self.v))
        
        patterns = []
        for l in self.chopped:
            patterns.append(self.make_ors(l))
        return patterns


class Range(PatternBase):
    negatable = True
    
    def __init__(self, pattern, negate=False, *args, **kwargs):
        self.v = pattern.v
        self.N = self.v.size
        self.is_un = pattern.is_un
        self.uni_steps = pattern.uni_steps
        self.U = pattern.U
        self.chopped = pattern.chopped
        self.negate = negate

    def make_range(self, l: str):
        # print(l)
        
        if len(l) == 1: #Stupid way
            index = self.U.index(l[0])            
            low = randrange(0,index+1)
            high = randrange(index,len(self.U))

            if self.negate:
                low_range = randrange(0, index) if low != index else index
                high_range = randrange(index+1, len(self.U)-1)                
                if index - low_range >= 3:
                    low = low_range
                    high = randrange(low+1, index)
                else:
                    low = high_range
                    high = randrange(low+1, len(self.U))

                
            return f'[{"^" if self.negate else ""}{self.U[low]}-{self.U[high]}]{"*" if np.random.uniform() < 0.50 else ""}'
        else:
            if self.negate: #Not sure if this is the right way to do this
                return "".join([self.make_range(letter) for letter in l])

            l = list(l)
            l.sort(key=lambda x: self.U.index(x))
            s_string = ''.join(l)
            low = randrange(0, self.U.index(s_string[0])+1)
            high = randrange(self.U.index(s_string[-1]), len(self.U))
            return f'[{self.U[low]}-{self.U[high]}]+'


    def make_pattern(self):
        # Think about base cases for this
        
        patterns = []
        for l in self.chopped:
            patterns.append(self.make_range(l))
        return patterns

class RangeSet(PatternBase):

    negatable = True

    def __init__(self, pattern, negate=False, *args, **kwargs):
        self.v = pattern.v
        self.N = self.v.size
        self.is_un = pattern.is_un
        self.uni_steps = pattern.uni_steps
        self.U = pattern.U
        self.chopped = pattern.chopped
        self.negate = negate

    def make_range(self, l: str, max_randoms=3):
        min_randoms = 1
        pattern = np.array([])
        if not self.negate:
            pattern = np.array(l)
        else:
            max_randoms = 6
            min_randoms = 4
        N = randrange(1, max_randoms)

        star = "" if len(l) == 1 and np.random.uniform() < 0.50 else "*"
        if len(l) != 1 and (np.random.uniform() < 0.50):
            star = "+"

        random_set = np.array(list(self.U))
        random_set = np.delete(random_set, [self.U.index(letter) for letter in l])
        np.random.shuffle(random_set)
        random_set = random_set[:N]

        pattern = np.append(pattern, random_set)
        np.random.shuffle(pattern)

        return f'[{"^" if self.negate else ""}{"".join(pattern)}]{star}'

    def make_pattern(self):

        patterns = []
        for l in self.chopped:
            patterns.append(self.make_range(l))
        return patterns


class Pattern(object):
    types = [ORS, SimpleORS, SimplePattern, Range, RangeSet]
    def chop(self):
        self.chopped = []
        if not self.is_un:
            n_chops = randrange(1, self.v.size) 
            
            slice_indices = sample(range(self.v.size), n_chops)
            slice_indices.sort()

            if slice_indices[0] == 0:
                del slice_indices[0]

            lower_index = 0
            for i in slice_indices:
                self.chopped.append(self.v[lower_index:i])
                lower_index = i
            self.chopped.append(self.v[lower_index:])        
        else:    
            for i in range(0, len(self.v), self.uni_steps):
                ss = self.v[i:i+self.uni_steps]
                self.chopped.append("".join(ss))

    def __init__(self, vector: np.array, degree=1, is_uniform=True, uni_steps=1, universal_set=string.ascii_uppercase, chopped=None, *args, **kwargs):
        self.v = vector
        self.N = vector.size
        self.is_un = is_uniform
        self.uni_steps = uni_steps
        self.U = universal_set
        self.patterns = []
        self.degree = degree
        if chopped:
            self.chopped = chopped
        else:
            self.chop()
        

    def generate_patterns(self):
        for _type in self.types:            
            self.type = _type(self)                        
            pattern = self.type.make_pattern()            
            self.patterns.append(pattern)
        self.patterns = [list(x) for x in zip(*self.patterns)]


    def set_pattern(self):
        pattern = [[] for _ in range(self.degree)]
        for choices in self.patterns:
            selection = sample(choices, self.degree)
            for i in range(self.degree):
                pattern[i].append(selection[i])

        self.pattern = ["".join(p) for p in pattern]


    def get_pattern(self):
        return self.pattern

if __name__ == "__main__":
    p = Pattern(np.array(['A', 'B', 'C', 'D', 'E', 'F']))
    p.generate_patterns()
    # pprint(p.patterns)
    p.set_pattern()
    pprint(p.get_pattern())

# We should validate the pattern once we start putting the individual patterns together into one pattern

# 1D - | A | B | C | D | E | F | <- [A-F]*
# 
#       (A|D|G)*
# 2D - | A | B | C | [A-B]+C?
    #  | D | E | F |
    #  | G | H | I |

    # TODO: Fix space handling