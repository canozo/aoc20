const readline = require('readline');
const fs = require('fs');
const { EOL } = require('os');

const FLOOR = '.';
const EMPTY = 'L';
const TAKEN = '#';

function sleep(ms) {
  return new Promise((resolve) => {
    setTimeout(resolve, ms);
  });
}

function clear() {
  readline.cursorTo(process.stdout, 0, 0);
  readline.clearLine(process.stdout, 0);
  readline.clearScreenDown(process.stdout);
}

function evolve(grid, y, x) {
  const seat = grid[y][x];

  if (seat === FLOOR) {
    return FLOOR;
  }

  const adjacent = [
    grid[y - 1][x - 1], // up-left
    grid[y - 1][x    ], // up
    grid[y - 1][x + 1], // up-right
    grid[y    ][x - 1], // left
    grid[y    ][x + 1], // right
    grid[y + 1][x - 1], // down-left
    grid[y + 1][x    ], // down
    grid[y + 1][x + 1], // down-right
  ];

  if (seat === EMPTY && !adjacent.includes(TAKEN)) {
    return TAKEN;
  }

  if (seat === TAKEN && adjacent.filter(seat => seat === TAKEN).length >= 4) {
    return EMPTY;
  }

  return seat;
}

function findSeat(grid, y, x, limitY, limitX, dirY, dirX) {
  y += dirY;
  x += dirX;
  while (y !== limitY && x !== limitX) {
    const seat = grid[y][x];
    if (seat === EMPTY || seat === TAKEN) {
      return seat;
    }
    y += dirY;
    x += dirX;
  }
  return FLOOR;
}

function evolveMKII(grid, y, x) {
  const seat = grid[y][x];

  if (seat === FLOOR) {
    return FLOOR;
  }

  const w = grid[0].length;
  const h = grid.length;

  const adjacent = [
    findSeat(grid, y, x, 0, 0, -1, -1), // up-left
    findSeat(grid, y, x, 0, 0, -1, 0),  // up
    findSeat(grid, y, x, 0, w, -1, 1),  // up-right
    findSeat(grid, y, x, 0, 0, 0, -1),  // left
    findSeat(grid, y, x, 0, w, 0, 1),   // right
    findSeat(grid, y, x, h, 0, 1, -1),  // down-left
    findSeat(grid, y, x, h, 0, 1, 0),   // down
    findSeat(grid, y, x, h, w, 1, 1),   // down-right
  ];

  if (seat === EMPTY && !adjacent.includes(TAKEN)) {
    return TAKEN;
  }

  if (seat === TAKEN && adjacent.filter(seat => seat === TAKEN).length >= 5) {
    return EMPTY;
  }

  return seat;
}

async function* solver(filename) {
  const layout = fs.readFileSync(filename)
    .toString()
    .split(EOL)
    .filter(row => row !== '')
    .map(row => `.${row}.`);

  const width = layout[0].length;

  layout.unshift('.'.repeat(width));
  layout.push('.'.repeat(width));

  // part 1
  let previous = [];
  let current = [...layout];
  while (previous.toString() !== current.toString()) {
    if (process.argv.includes('log')) {
      clear();
      process.stdout.write(current.join('\n'));
      await sleep(75);
    }

    previous = [...current];

    for (let i = 1; i < layout.length - 1; i += 1) {
      const row = [];
      for (let j = 1; j < width - 1; j += 1) {
        row.push(evolve(previous, i, j));
      }
      current[i] = `.${row.join('')}.`;
    }
  }

  yield current.reduce((acc, row) => acc + (row.match(new RegExp(TAKEN, 'g')) || []).length, 0);

  // part 2
  previous = [];
  current = [...layout];
  while (previous.toString() !== current.toString()) {
    if (process.argv.includes('log')) {
      clear();
      process.stdout.write(current.join('\n'));
      await sleep(75);
    }

    previous = [...current];

    for (let i = 1; i < layout.length - 1; i += 1) {
      const row = [];
      for (let j = 1; j < width - 1; j += 1) {
        row.push(evolveMKII(previous, i, j));
      }
      current[i] = `.${row.join('')}.`;
    }
  }

  yield current.reduce((acc, row) => acc + (row.match(new RegExp(TAKEN, 'g')) || []).length, 0);
}

(async () => {
  if (!process.argv.includes('log')) {
    process.stdout.write('use arg "log" to show seat changes.');
  }

  let part = 1;
  let solution;
  const solutions = solver('input.txt');
  while ((solution = await solutions.next()) && solution.value) {
    process.stdout.write(`\npart${part} answer: ${solution.value}`);
    part += 1;
  }
})();
