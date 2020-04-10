from grid import Puzzle
from pattern import Pattern
import numpy as np
from pprint import pprint

# puzzle = Puzzle('TEST')
# puzzle = Puzzle('assume,foodee,nation')


# vectors = puzzle.vectors
# pprint(vectors)

def generate_patterns(vectors):

    f_patterns = []

    for s in range(vectors.shape[-1]):
        # transpose_matrix = np.roll(list(range(vectors.shape[-1])), s)
        transpose_matrix = np.roll(list(range(vectors.ndim)), s)

        patterns = []
        for x in vectors.transpose(transpose_matrix):
            pats = []
            for v in x:
                pat = Pattern(v)
                pat.generate_patterns()
                pat.set_pattern()
                pats.append(pat.get_pattern()[0])
            patterns.append(pats)
        f_patterns.append(patterns)
        if vectors.shape[:2] == (1, 1): # YIKES this is not gud
            print("1D Vector! No need to transpose")
            break

    return f_patterns

# f_patterns = generate_patterns(vectors)

# Manual example
"""
# These two are gud
print(vectors[1][1][-1])
# round 1
# position : 1, 1, 2
print(f_patterns[0][1][1])
#round 2
# position : 2, 1, 1
print(f_patterns[1][2][1])
#round 3
# position : 1, 2, 1
print(f_patterns[2][1][2])
"""

# Found that we're simpy shifting coords of the letter based on the direction which is the first index in the f_patterns matrix, 
# this comes as a result of transposing the matrix by rolling the transpose matrix in the generate function
print(vectors[0][0][1])
def get_patterns(coords, patterns):
    diff = len(coords) - len(patterns) # I don't know why we need this, but it makes things work.
    N = len(coords)
    # N = len(patterns)
    pcoords = [np.roll(coords, i)[:N-1] for i in range(N-diff)] # construct the direction vector coordinates for each pattern vector
    print(pcoords)
    patterns = [patterns[x][i][j] for x, (i, j) in enumerate(pcoords)]
    return patterns

# p = get_patterns([0, 0, 0], f_patterns)
# pprint(p)