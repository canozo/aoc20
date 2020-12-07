#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int countLetters(int group[26])
{
    int result = 0;
    for (int i = 0; i < 26; i += 1)
    {
        if (group[i] == 1)
        {
            result += 1;
            printf("%c", i + 97);
        }
        else
        {
            printf(" ");
        }
    }
    printf("\n");
    return result;
}

int main(int argc, char *argv[])
{
    // get filename and part number from args
    char *filename = "input.txt";
    int part = 1;
    if (argc > 2)
    {
        filename = argv[1];
        part = atoi(argv[2]);
    }

    // try to open file
    FILE *file = fopen(filename, "r");
    if (file == NULL)
    {
        printf("Couldn't open file %s.", filename);
        return 1;
    }

    int count = 0;
    int group[26] = {0};

    // read file line by line
    char line[28];
    while (fgets(line, sizeof(line), file))
    {
        // remove newline
        int len = strlen(line) - 1;
        line[len] = 0;

        // check line if is empty (new group)
        if (strcmp(line, "") == 0)
        {
            count += countLetters(group);
            memset(group, 0, sizeof(group));
            continue;
        }

        if (part == 1)
        {
            for (int i = 0; i < len; i += 1)
            {
                group[line[i] - 97] = 1;
            }
        }
        else if (part == 2)
        {
            for (int i = 0; i < 26; i += 1)
            {
                group[i] = strchr(line, i + 97) && (!group[i] || group[i] == 1) ? 1 : 666;
            }
        }
    }

    // process the last group
    count += countLetters(group);

    printf("count: %d\n", count);

    fclose(file);
    return 0;
}
