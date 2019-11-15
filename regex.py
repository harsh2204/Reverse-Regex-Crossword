from grid import Puzzle
from pattern import Pattern

puzzle = Puzzle()

shape = puzzle.vectors.shape

row_patterns = []
col_patterns = []

print(shape)
print("ROWS")
for i in range(shape[0]):
    a = puzzle.vectors[i]
    print(a)
    p_n = Pattern(a)
    p_n.generate_patterns()
    p_n.set_pattern()
    row_patterns.append(p_n.get_pattern())


print("COLS")
for i in range(shape[1]):
    a = puzzle.vectors[:,i]
    print(a)
    p_n = Pattern(a)
    p_n.generate_patterns()
    p_n.set_pattern()
    col_patterns.append(p_n.get_pattern())

# 3D version can be implemented just by using the above for loop on the third dimension. 
# There is no good way to visualize this right now, so I guess the next step forward would be to make a visualizer.
# TODO: Make a good ass visualizer. And fix 1D and 2D cases LOL


[print(r[0]) for r in row_patterns]
[print(c[0]) for c in col_patterns]
