from grid import Puzzle
from pattern import Pattern

# puzzle = Puzzle('TEST,FOUR')
puzzle = Puzzle('assume,foodee,nation')

shape = puzzle.vectors.shape

row_patterns = []
col_patterns = []
bro_patterns = []

print(shape)
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
