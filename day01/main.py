from itertools import combinations

def mul(values):
    result = 1
    for value in iter(values):
        result *= value
    return result

def solution(input_file, size):
    with open(input_file, 'r') as file:
        for raw_values in combinations(file.readlines(), size):
            values = list(map(lambda x: int(x.strip('\n')), raw_values))
            if sum(values) == 2020:
                return mul(values)
    return 0

print(f'Answer: {solution("example.txt", 2)}')
print(f'Answer: {solution("input.txt", 2)}')

print(f'Answer: {solution("example.txt", 3)}')
print(f'Answer: {solution("input.txt", 3)}')
