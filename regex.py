import re
import os
import random
# pat = 'HE|LL|O+'
# pat = '[^SPEAK]+'

# try :
#     a = re.compile(pat)
#     print("regex compiled successfuly.")
# except:
#     print("regex compilation failed.")



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

def draw_grid(s:str):
    n = len(s)
    if n%2:
        print("String not compatible due to odd length:", n)
        return
    
    
    combs = []
    if len(s) <= 4:
        combs.append(set([len(s)//2, len(s)//2]))
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
    for c, v in enumerate(combs, 1):
        x, y = v if len(v) == 2 else list(v)[0], list(v)[0]
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
    if len(selection) > 1:
        choices = [
            re.findall('.{1,'+str(selection[0])+'}', s),
            re.findall('.{1,'+str(selection[1])+'}', s)
        ]
        selection = [str(x) for x in selection]
        print("\n[0]", " x ".join(selection))
        print_grid(choices[0])
        selection.reverse()
        print("\n[1]", " x ".join(selection))
        print_grid(choices[1])
        ori = input("Please select an orientation for the grid: ")
        x, y = choices[int(ori)]
        rows = re.findall('.{1,'+str(x)+'}', s)
    # print(rows)    


# random_words = open('accepted_words').read().split("\n")
# sel = random.choice(random_words)
# print("@"+sel+"@")
draw_grid("four")