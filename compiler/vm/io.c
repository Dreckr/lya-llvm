#include <stdio.h>

void print_int(int value) {
    printf("%d\n", value);
}


void print_bool(int value) {
    if (value > 0) {
        printf("true\n");
    } else {
        printf("false\n");
    }
}