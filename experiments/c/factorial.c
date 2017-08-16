#include <stdio.h>

int x;

int fat(int n) {
    if (n == 0) {
        return 1;
    } else {
        return n * fat(n - 1);
    }
}

int main() {
    printf("give-me a positive integer:\n");

    scanf("%d", &x);

    printf("factorial of %d = %d\n", x, fat(x));

    return 0;
}
