from grid import Puzzle
from pattern import Pattern
import numpy as np
from pprint import pprint

# puzzle = Puzzle('TEST,FOUR')
puzzle = Puzzle('assume,foodee,nation')

shape = puzzle.vectors.shape

row_patterns = []
col_patterns = []
bro_patterns = []
f_patterns = []

print(shape)
vectors = puzzle.vectors
for s in range(vectors.shape[-1]):
    transpose_matrix = np.roll(list(range(vectors.shape[-1])), s)
    print(transpose_matrix)
    patterns = []
    for x in vectors.transpose(transpose_matrix):
        print(x)
        pats = []
        for v in x:
            pat = Pattern(v)
            pat.generate_patterns()
            pat.set_pattern()
            pats.append(pat.get_pattern()[0])
        patterns.append(pats)
    print("*"*50)
    f_patterns.append(patterns)

print("*"*50)
pprint(f_patterns)

# These two are gud
# position : 1, 1, 2
print(f_patterns[0][1][1])
print(vectors[1][1][-1])

#round 2
# position : 2, 1, 1
print(f_patterns[1][2][1])
#round 3
# position : 1, 2, 1
print(f_patterns[2][1][2])
# Found that we're simpy shifting coords of the letter based on the direction which is the first index in the f_patterns matrix
exit()

print("ROWS")
for a in puzzle.vectors.transpose(0, 1, 2):
    # print("*"*50)
    # print(a)
    # print("*"*50)
    for v in a:
        p_n = Pattern(v)
        p_n.generate_patterns()
        p_n.set_pattern()
        row_patterns.append(p_n.get_pattern())
        print(v, p_n.get_pattern())


print("COLS")
for a in puzzle.vectors.transpose(2, 0, 1):
    # print("*"*50)
    # print(a)
    # print("*"*50)
    for v in a:        
        p_n = Pattern(v)
        p_n.generate_patterns()
        p_n.set_pattern()
        col_patterns.append(p_n.get_pattern())
        print(v, p_n.get_pattern())


print("BROS")
for a in puzzle.vectors.transpose(1, 2, 0):
    # print("*"*50)
    # print(a)
    # print("*"*50)
    for v in a:        
        p_n = Pattern(v)
        p_n.generate_patterns()
        p_n.set_pattern()
        bro_patterns.append(p_n.get_pattern())
        print(v, p_n.get_pattern())
# 3D version can be implemented just by using the above for loop on the third dimension. 
# There is no good way to visualize this right now, so I guess the next step forward would be to make a visualizer.
# TODO: Make a good ass visualizer. And fix 1D and 2D cases LOL
