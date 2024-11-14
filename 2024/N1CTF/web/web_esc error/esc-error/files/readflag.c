#include <stdio.h>

int main() {
    FILE *file = fopen("/flag", "r");

    if (file == NULL) {
        printf("failed to open /flag\n");
        return 1;
    }

    int ch;
    while ((ch = fgetc(file)) != EOF) {
        putchar(ch);
    }

    fclose(file);
    return 0;
}
