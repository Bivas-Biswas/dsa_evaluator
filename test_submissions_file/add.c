#include <stdio.h>
int main(int argc, char* argv[]) {
    FILE *in = fopen(argv[1], "r");
    FILE *out = fopen(argv[2], "w");
    int a, b;
    fscanf(in, "%d %d", &a, &b);
    fprintf(out, "%d\n", a + b);
    fclose(in);
    fclose(out);
    return 0;
}