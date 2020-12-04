def v1(input_file):
    with open(input_file, 'r') as file:
        lines = file.readlines()
        for i, first_line in enumerate(lines):
            first = int(first_line.strip('\n'))
            for j, second_line in enumerate(lines):
                second = int(second_line.strip('\n'))
                if i != j and first + second == 2020:
                    return first * second

    return 0

def v2(input_file):
    with open(input_file, 'r') as file:
        lines = file.readlines()
        for i, first_line in enumerate(lines):
            first = int(first_line.strip('\n'))
            for j, second_line in enumerate(lines):
                second = int(second_line.strip('\n'))
                for k, third_line in enumerate(lines):
                    third = int(third_line.strip('\n'))
                    if i != j != k and first + second + third == 2020:
                        return first * second * third
    return 0

# print(f'Answer: {v1("example.txt")}')
# print(f'Answer: {v1("input.txt")}')

# print(f'Answer: {v2("example.txt")}')
print(f'Answer: {v2("input.txt")}')
