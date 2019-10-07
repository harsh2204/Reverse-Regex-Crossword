import numpy as np
from random import randrange, sample
import string


class PatternBase(object):
    def __init__(self, vector: np.array, is_uniform=True, uni_steps=1, *args, **kwargs):
        self.v = vector
        self.N = vector.size
        self.is_un = is_uniform
        self.uni_steps = uni_steps
            
    def chop(self):
        if not self.is_un:
            n_chops = randrange(1, self.v.size)        
            
            slice_indices = sample(range(self.v.size), n_chops)

            slice_indices.sort()
            # print(n_chops, slice_indices)

            if slice_indices[0] == 0:
                del slice_indices[0]

            chopped = []
            lower_index = 0
            for i in slice_indices:
                chopped.append(self.v[lower_index:i])
                lower_index = i
            chopped.append(self.v[lower_index:])
            # print(chopped)
            return chopped
        else:
            chopped = []
            for i in range(0, len(self.v), self.uni_steps):
                ss = self.v[i:i+self.uni_steps]
                chopped.append("".join(ss))
            return chopped

class SimplePattern(PatternBase):
    def make_pattern(self):
        chopped = self.chop()
        if not self.is_un:
            chopped = ["".join(x) for x in chopped]
        return chopped

class SimpleORS(PatternBase):
    def make_pattern(self):
        # we will make a random or dup and concatenate it as, rand|letter. 
        
        patterns = []
        self.chopped = self.chop()

        for l in self.chopped:
            alphabet = string.ascii_uppercase
            random_set = np.array(list(alphabet))         
            np.random.shuffle(random_set)
            random_set = random_set[:self.uni_steps]
            random_string = "".join(list(random_set))
            if l == random_string:
                random_string = chr((ord(l[0]) + 1)) + l[1:] if ord(l[0]) + 1 < 90 else 'A' + l[1:]

            p = f'{random_string}|{l}' if np.random.uniform() < 0.50 else f'{l}|{random_string}'
            patterns.append(p)
        return patterns

class ORS(PatternBase):

    def __init__(self, vector: np.array, is_uniform=False, *args, **kwargs):
        self.v = vector
        self.N = vector.size
        self.is_un = is_uniform        

    @staticmethod
    def make_ors(l: str, max_randoms=3):
        # make a random ne  of N terms where l is appended, and the set is shuffled. 
        # alternatively we could use a random index to append tothe set  which would bring down the iterations.
        # Note: we must make sure that we don't have l in our randomly selected set of N terms.

        # if (v.size - max_randoms) > 2
        pattern = np.array(l)
        N = randrange(1, max_randoms)
        
        star = "" if l.size == 1 and np.random.uniform() < 0.50 else "*"
        if l.size != 1 and (np.random.uniform() < 0.50):
            star = "+"
            
        alphabet = string.ascii_uppercase
        random_set = np.array(list(alphabet))
        random_set = np.delete(random_set, [ord(letter)-65 for letter in l])
        np.random.shuffle(random_set)
        random_set = random_set[:N]

        pattern = np.append(pattern, random_set)
        np.random.shuffle(pattern)
        return f"({'|'.join(list(pattern))}){star}"

        
    def make_pattern(self):
        if self.N < 3:
            return "".join(list(self.v))
        
        gap = randrange(2, self.N) 
        offset = randrange(self.N - gap + 1)

        ors = self.v[offset:offset + gap]
        remainder = np.setdiff1d(self.v, ors)

        # print(gap, offset, ors, remainder)
        
        self.chopped = self.chop()
        patterns = []
        for l in self.chopped:
            patterns.append(self.make_ors(l))
        return patterns

class Pattern(object):
    
    def __init__(self, vector: np.array, *args, **kwargs):
        self.v = vector        
        self.type = ORS(vector) 
        # Figure out 
    def get_pattern(self):
        for type in [ORS,SimpleORS, SimplePattern]:
            self.type = type(self.v)
            print(type.__name__)
            self.pattern = self.type.make_pattern()
            if type.__name__ == "ORS":
                print('Chopped: ',[list(x) for x in self.type.chopped], end=" ")
            print(self.pattern)

        return self.pattern 

p = Pattern(np.array(['A', 'B', 'C', 'D', 'E', 'F']))
p.get_pattern()