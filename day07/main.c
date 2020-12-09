#include <stdio.h>
#include <stdlib.h>
#include <assert.h>
#include <string.h>

#define MAX_NODES 1024
#define MAX_LINKS 16
#define MAX_COLOR 32

// type and structure definitions
typedef struct graph graph_t;
typedef struct node node_t;
typedef struct link link_t;

struct graph
{
    int size;
    node_t *nodes[MAX_NODES];
};

struct node
{
    char name[MAX_COLOR];
    int marked;
    int size_parents;
    link_t *parents[MAX_LINKS];
    int size_children;
    link_t *children[MAX_LINKS];
};

struct link
{
    int weight;
    node_t *next;
};

void delete_node(node_t *);
void delete_link(link_t *);
node_t *new_node(char *, graph_t *);
link_t *new_link(node_t *, int);

/* ------------------------------ GRAPH ------------------------------ */
graph_t *new_graph()
{
    graph_t *this = malloc(sizeof(*this));
    this->size = 0;
    return this;
}

void delete_graph(graph_t *this)
{
    for (int i = 0; i < this->size; i += 1)
    {
        delete_node(this->nodes[i]);
    }
    free(this);
}

void graph_add_node(graph_t *this, node_t *node)
{
    assert(this->size+1 < MAX_NODES);
    this->nodes[this->size] = node;
    this->size += 1;
}

node_t *graph_find_node(graph_t *this, char *name)
{
    for (int i = 0; i < this->size; i += 1)
    {
        if (strcmp(this->nodes[i]->name, name) == 0)
        {
            return this->nodes[i];
        }
    }
    return NULL;
}

node_t *graph_create_node_if_not_exists(graph_t *this, char *name)
{
    node_t *node = graph_find_node(this, name);
    if (!node)
    {
        node = new_node(name, this);
    }
    return node;
}

/* ------------------------------ NODE ------------------------------ */
node_t *new_node(char *name, graph_t *graph)
{
    node_t *this = malloc(sizeof(*this));
    strcpy(this->name, name);
    this->marked = 0;
    this->size_parents = 0;
    this->size_children = 0;
    graph_add_node(graph, this);
    return this;
}

void delete_node(node_t *this)
{
    for (int i = 0; i < this->size_parents; i += 1)
    {
        delete_link(this->parents[i]);
    }
    for (int i = 0; i < this->size_children; i += 1)
    {
        delete_link(this->children[i]);
    }
    free(this);
}

void node_add_parent(node_t *this, node_t *parent, int weight)
{
    assert(this->size_parents+1 < MAX_LINKS);
    this->parents[this->size_parents] = new_link(parent, weight);
    this->size_parents += 1;
}

void node_add_child(node_t *this, node_t *child, int weight)
{
    assert(this->size_children+1 < MAX_LINKS);
    this->children[this->size_children] = new_link(child, weight);
    this->size_children += 1;
}

int node_travel_parents(node_t *this, int depth)
{
    int w = 2 * depth;
    int traveled = 0;
    if (!this->marked)
    {
        traveled += 1;
        this->marked = 1;
        for (int i = 0; i < this->size_parents; i += 1)
        {
            node_t *parent = this->parents[i]->next;
            traveled += node_travel_parents(parent, depth + 1);
        }
    }
    return traveled;
}

int node_count_children(node_t *this, int parent_bags, int depth)
{
    int w = 2 * depth;
    int bags = 0;
    for (int i = 0; i < this->size_children; i += 1)
    {
        link_t *link = this->children[i];
        int prod = link->weight * parent_bags;
        bags += prod + node_count_children(link->next, prod, depth + 1);
    }
    return bags;
}

/* ------------------------------ LINK ------------------------------ */
link_t *new_link(node_t *next, int weight)
{
    link_t *this = malloc(sizeof(*this));
    this->weight = weight;
    this->next = next;
    return this;
}

void delete_link(link_t *this)
{
    free(this);
}

/* ------------------------------ MAIN ------------------------------ */
int main(int argc, char *argv[])
{
    char *filename = "input.txt";
    if (argc > 1)
    {
        filename = argv[1];
    }

    FILE *file = fopen(filename, "r");
    if (file == NULL)
    {
        fprintf(stderr, "Couldn't open file %s.", filename);
        return 1;
    }

    graph_t *graph = new_graph();

    char line[128];
    while (fgets(line, sizeof(line), file))
    {
        // remove newline and dot at the end
        line[strlen(line) - 2] = 0;

        char *color_delim = strstr(line, " bags contain");
        color_delim[0] = 0;

        char color[MAX_COLOR];
        strcpy(color, line);

        color_delim[0] = ' ';

        node_t *container = graph_create_node_if_not_exists(graph, color);

        if (strstr(line, "no other bags"))
        {
            continue;
        }

        char *contents = line + strlen(color) + 13;
        char *content = strtok(contents, ",");
        do
        {
            int amount = content[1] - '0';
            content += 3;
            strstr(content, " bag")[0] = 0;

            node_t *neighbor = graph_create_node_if_not_exists(graph, content);
            node_add_parent(neighbor, container, amount);
            node_add_child(container, neighbor, amount);
        }
        while (content = strtok(NULL, ","));
    }

    node_t *shiny_gold = graph_find_node(graph, "shiny gold");
    printf("bags that contain shiny gold: %d\n", node_travel_parents(shiny_gold, 1) - 1);
    printf("bags inside shiny gold: %d\n", node_count_children(shiny_gold, 1, 1));

    delete_graph(graph);
    fclose(file);
    return 0;
}
