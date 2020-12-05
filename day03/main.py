def solution(input_file, slope):
    tree_count = 0
    with open(input_file, 'r') as file:
        tree_grid = list(map(lambda x: x.strip('\n'), file.readlines()))
        repeat_len = len(tree_grid[0])

        inc_x, inc_y = slope
        slope_x, slope_y = slope
        while slope_y < len(tree_grid):
            if tree_grid[slope_y][slope_x % repeat_len] == '#':
                tree_count += 1
            slope_x += inc_x
            slope_y += inc_y
    return tree_count

def min_slope(input_file):
    slopes = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]
    result = 1
    for slope in slopes:
        result *= solution(input_file, slope)
    return result

print(f'Tree count in example: {solution("example.txt", (3, 1))}')
print(f'Tree count in input: {solution("input.txt", (3, 1))}')

print(f'Min slopes in example: {min_slope("example.txt")}')
print(f'Min slopes in input: {min_slope("input.txt")}')
