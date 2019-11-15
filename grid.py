import re
import os
import random
from math import sqrt
import numpy as np


class Puzzle(object):
     
     
    @staticmethod
    def is_square(words):
        return all([len(n)%2 == 0 or sqrt(len(n)).is_integer() for n in words])


    def __init__(self, words=None, use_default=True): #TODO Complete this after patterns
        if words:
            self.words = words            
            if not self.is_square(words):
                print("Entered word(s) are not square")
                return None
        else:
            self.setup_grid(use_default)

    @staticmethod
    def print_empty_grid(x, y):
        print("+"+"--+"*x)
        for _ in range(y):
            for _ in range(x):
                print("|  ", end='')
            print("|")                        
            print("+"+"--+"*x)    
    
    def print_grid(self, l):          
        x = len(l[0])
        print("+"+"--+"*x)
        for row in l:
            print("|"+" |".join(list(row)), end = '')
            print(" |")                        
            print("+"+"--+"*x)

    def setup_grid(self, use_default=True):
        words = input("Please enter the puzzle string(s), separated by commas (,) without extra white space if more than one.\n").split(',')
        words = [w.upper() for w in words]
        if not self.is_square(words):
            print("String not compatible due to odd length:", len(words[0]))
            return
        
        deg = len(words)
                        
        s = words[0]

        if deg > 1:                                
            max_len = len(max(words, key=len))
            min_len = len(min(words, key=len))
            if max_len != min_len:
                print(f"There was missmatch in lengths of strings inside your puzzle. The shortest string has {min_len} whereas the longest string has {max_len} letters")
                response = ""
                while not use_default and response.lower() not in ['y', 'n']:
                    response = input(f"Would you like to fill the remaining characters with blank spaces?\n").lower()
                if use_default or response == 'y':
                    for i in range(len(words)):
                        cur_len = len(words[i])
                        if cur_len < max_len:
                            words[i] = words[i] + " "*(max_len-cur_len)
                        print(f"*{words[i]}*")

            top_string = words[0]

            if not use_default:    
                print("The default degree for every vector is 1, meaning every vector/row will have only one pattern as a clue. You can change this value now if you'd like")
                degree = input("Please enter a degree (1-n): ")
                if degree.isnumeric() and int(degree) > 0:
                    print("Changing degree to", degree)
                    self.degree = degree

                print("Given the higher dimensional string input, please select a sensible plane string")
                response = None
                for i, v in enumerate(words, 1):
                    print(f"[{i}] {v.upper()}")
                
                while response not in range(1, len(words)+1):
                    response = int(input(f"Please select a string in range(1-{len(words)}): "))
                
                top_string = words[response-1]
            else:
                print("Defaulting to 1\n")
                self.degree = 2 if deg > 1 else 1
            
            s = top_string
        self.top_string = s

        n = len(s)        

        combs = []
        if n <= 4:
            combs.append(set([n//2, n//2]))
        for j in range(2,n//2):            
            tup = set([j, n//j])
            if n%j==0 and tup not in combs:
                combs.append(tup)
        

        if len(combs) == 0:
            print("Could not find any combinations")
            return

        # os.system('cls' if os.name == 'nt' else 'clear')
        selection = list(combs[-1])
        if not use_default:
            for c, v in enumerate(combs, 1):
                if len(v) == 1:
                    v = list(v)*2
                x, y = v
                print(f'[{c}] {x} x {y} grid')
                rows = []
                if x < y:
                    rows = re.findall('.{1,'+str(y)+'}', s)        
                else:
                    rows = re.findall('.{1,'+str(x)+'}', s)        
                self.print_grid(rows)

            resp = input('Please select a configuration for the crossword (the number inside []): ')


            assert resp.isdigit(), "Please enter an integer!"
            resp = int(resp)

            assert resp<=len(combs), f"Please enter a value in range 1, {str(len(combs))}"

            os.system('cls' if os.name == 'nt' else 'clear')
            selection = list(combs[resp-1])

        l_splitted = [re.findall('.{1,'+str(selection[0])+'}', w) for w in words] #Still have no clue why I'm using a list for selection here...

        vectors = []
        for v in l_splitted:            
            d_array = [list(x) for x in v]
            vectors.append(np.array(d_array))        
        
        self.vectors = np.dstack(vectors)
        print(self.vectors)
        # Setup the final grid with the correct dimensions and spaces.
        # We still need to split all the other vectors before we construct the final grid.
        # Eventually, we can start packing letters to accomodate the input words.

        
        # rows = [np.array(row) for row in rows]
        
        # self.vectors = np.array(rows)
        # return self.vectors
        # return an n dimensional array of letters

if __name__ == "__main__":
    g = Puzzle()
    
    #assume,food,national
    #assume,foodee,nation