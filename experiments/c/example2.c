#include <stdio.h>

void g (int t);

int z, t;

int main() {
    z = 4;
    t = 4;

    g(t); printf("%d %d\n", z, t);
    g(z); printf("%d %d\n", z, t);
    g(t+z); printf("%d %d\n", z, t);
    g(7); printf("%d %d\n", z, t);

    return 0;
}

void g (int t) {
    int x;

    t *= 2;
    x = 2 * t;
    z = x + 1;
}
