def v1(input_file):
    with open(input_file, 'r') as file:
        instructions = list(map(lambda x: x.rstrip('\n'), file))
        acc = 0
        pos = 0
        visited = []

        while pos < len(instructions):
            if pos in visited:
                return acc
            visited.append(pos)
            op, value = instructions[pos].split(' ')
            value = int(value)

            if op == 'acc':
                acc += value
            elif op == 'jmp':
                pos += value
                continue

            pos += 1

def v2(input_file):
    with open(input_file, 'r') as file:
        instructions = list(map(lambda x: x.rstrip('\n'), file))
        replace = 0

        while True:
            acc = 0
            pos = 0
            visited = []

            while pos < len(instructions):
                if pos in visited:
                    break
                visited.append(pos)
                op, value = instructions[pos].split(' ')
                value = int(value)

                # replace jmp or nop
                if replace == pos and op == 'jmp':
                    op = 'nop'
                elif replace == pos and op == 'nop':
                    op = 'jmp'

                if op == 'acc':
                    acc += value
                elif op == 'jmp':
                    pos += value
                    continue

                pos += 1

            if pos == len(instructions):
                return acc

            replace += 1

print(f'[part 1] answer in input: {v1("input.txt")}')
print(f'[part 1] answer in example: {v1("example.txt")}')

print(f'[part 2] answer in input: {v2("input.txt")}')
print(f'[part 2] answer in example: {v2("example.txt")}')
