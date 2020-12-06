#include <stdio.h>
#include <assert.h>

int main(int argc, char *argv[])
{
    // get filename from args
    char *filename;
    if (argc <= 1)
    {
        filename = "input.txt";
    }
    else
    {
        filename = argv[1];
    }

    // try to open file
    FILE *file = fopen(filename, "r");
    if (file == NULL)
    {
        printf("Couldn't open file %s.", filename);
        return 1;
    }

    // we are looking for the highest seat id
    // seat id = row * 8 + column
    int maxSeatId = 0;
    int minSeatId = 999;

    // store an array of flags to know if the seatid was set or not
    // we'll take the size of 1024 even though it might be as low as 816
    int seats[1024] = {0};

    // read file line by line
    char line[12];
    while (fgets(line, sizeof(line), file))
    {
        // set the newline character to NULL
        line[10] = 0;

        // we need to know the lower and upper limit of the seats when
        // doing the divison process, ex: low => 64, high => 127

        // NOTE: 127 / 2 = 63

        // there are 128 rows
        int rowLow = 0;
        int rowHigh = 127;

        // there are 8 columns
        int colLow = 0;
        int colHigh = 7;

        for (int i = 0; i < 10; i += 1)
        {
            // first seven characters are either 'F' or 'B'
            if (line[i] == 'F')
            {
                // keep lower half
                rowHigh = rowLow + (rowHigh - rowLow) / 2;
            }
            else if (line[i] == 'B')
            {
                // keep upper half
                rowLow = rowHigh - (rowHigh - rowLow) / 2;
            }

            // last three characters are either 'L' or 'R'
            else if (line[i] == 'L')
            {
                // keep lower half
                colHigh = colLow + (colHigh - colLow) / 2;
            }
            else if (line[i] == 'R')
            {
                // keep upper half
                colLow = colHigh - (colHigh - colLow) / 2;
            }
        }

        assert(rowLow == rowHigh);
        assert(colLow == colHigh);

        int seatId = rowLow * 8 + colLow;
        printf("seat id = %d\n", seatId);

        if (seatId > maxSeatId)
        {
            maxSeatId = seatId;
        }

        if (seatId < minSeatId)
        {
            minSeatId = seatId;
        }

        seats[seatId] = 1;
    }

    printf("max seat id = %d\n", maxSeatId);
    printf("min seat id = %d\n", minSeatId);

    // part 2:
    // if I understand correctly, we have to mark all the seats and
    // our seat should be the only one missing on the list
    for (int i = minSeatId; i < maxSeatId; i += 1)
    {
        if (!seats[i])
        {
            printf("empty seat: %d\n", i);
        }
    }

    fclose(file);
    return 0;
}
