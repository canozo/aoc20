def solver(filename):
    with open(filename, 'r') as file:
        puzzle = list(map(lambda x: int(x.strip('\n')), file.readlines()))
        puzzle.sort()
        puzzle = [0] + puzzle + [puzzle[-1] + 3]

    curr = 0
    diffs = {
        1: 0,
        3: 0,
    }

    for i in range(1, len(puzzle)):
        number = puzzle[i]
        diffs[number - curr] += 1
        curr = number

    yield diffs[1] * diffs[3]

    past_solutions = [1]
    for i in range(1, len(puzzle)):
        solution = 0
        for j in range(i):
            if puzzle[i] - puzzle[j] <= 3:
                solution += past_solutions[j]
        past_solutions.append(solution)

    yield past_solutions[-1]

solutions = solver('input.txt')
for part, solution in enumerate(solutions):
    print(f'part{part + 1} answer: {solution}')
