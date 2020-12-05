import re

def v1(input_file):
    result = 0
    with open(input_file, 'r') as file:
        # minimum-maximum char: pw
        for unstripped_line in file:
            line = unstripped_line.strip('\n')
            instructs, pw = line.split(': ')
            limits, char = instructs.split(' ')
            minimum, maximum = map(int, limits.split('-'))
            if minimum <= pw.count(char) <= maximum:
                result += 1
    return result

def v2(input_file):
    result = 0
    with open(input_file, 'r') as file:
        # pos1-pos2 char: pw
        for unstripped_line in file:
            line = unstripped_line.strip('\n')
            instructs, pw = line.split(': ')
            limits, char = instructs.split(' ')
            # notice: there's no index 0, substract 1
            pos1, pos2 = map(lambda x: int(x) - 1, limits.split('-'))
            if pw[pos1] != pw[pos2] and (pw[pos1] == char or pw[pos2] == char):
                result += 1
    return result

# print(f'Valid passwords: {v1("example.txt")}')
# print(f'Valid passwords: {v1("input.txt")}')

# print(f'Valid passwords: {v2("example.txt")}')
print(f'Valid passwords: {v2("input.txt")}')
