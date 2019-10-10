import re
import os
import random
from math import sqrt
import numpy as np


class Grid():

    def __init__(self, words, grid_size): #TODO Complete this after patterns
        if len(args == 0):
            print("Starting automatic interactive grid setup")

        self.is_square = sqrt(n).is_integer()
        return 

    def print_empty_grid(x, y):    
        print("+"+"--+"*x)
        for _ in range(y):
            for _ in range(x):
                print("|  ", end='')
            print("|")                        
            print("+"+"--+"*x)    

    def print_grid(l: list):    
        x = len(l[0])
        print("+"+"--+"*x)
        for row in l:
            print("|"+" |".join(list(row)), end = '')
            print(" |")                        
            print("+"+"--+"*x)  

    def setup_grid(s:str, use_default=True):
        n = len(s)
        if n%2 and not is_square(n):
            print("String not compatible due to odd length:", n)
            return
        
        
        combs = []
        if n <= 4:
            combs.append(set([n//2, n//2]))
        for j in range(2,n//2):
            print(j)
            tup = set([j, n//j])
            if n%j==0 and tup not in combs:
                combs.append(tup)
        
        print(combs)
        if len(combs) == 0:
            print("Could not find any combinations")
            return

        os.system('cls' if os.name == 'nt' else 'clear')
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
                print_grid(rows)

            resp = input('Please select a configuration for the crossword (the number inside []): ')

            assert resp.isdigit(), "Please enter an integer!"
            resp = int(resp)

            assert resp<=len(combs), f"Please enter a value in range 1, {str(len(combs))}"

            os.system('cls' if os.name == 'nt' else 'clear')
            selection = list(combs[resp-1])    

        rows = []
        if len(selection) > 1:
            choices = [
                re.findall('.{1,'+str(selection[0])+'}', s),
                re.findall('.{1,'+str(selection[1])+'}', s)
            ]
            if not use_default:
                selection = [str(x) for x in selection]
                print("\n[0]", " x ".join(selection))
                print_grid(choices[0])
                selection.reverse()
                print("\n[1]", " x ".join(selection))
                print_grid(choices[1])
                ori = input("Please select an orientation for the grid: ")        
            else:
                ori = 0
            rows = choices[int(ori)]        

        else:
            rows = re.findall('.{1,'+str(selection[0])+'}', s)
            
        rows = [list(x) for x in rows]
        return np.array(rows)
