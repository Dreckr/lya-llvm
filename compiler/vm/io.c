#include <string.h>
#include <stdio.h>

void print_int(int value) {
    printf("%d", value);
}

void print_bool(char value) {
    if (value > 0) {
        printf("true");
    } else {
        printf("false");
    }
}

void print_char(char value) {
    printf("%c", value);
}

void print_str(char *str) {
    printf("%s", str);
}

void println() {
    printf("\n");
}

void read_int(int *value) {
    scanf("%d", value);
}

void read_char(char *value) {
    scanf("%c", value);
}

void read_bool(char *value) {
    char input[255];
    scanf("%s", input);

    if (!strcmp(input, "true")) {
        *value = 1;
    } else {
        *value = 0;
    }
}
