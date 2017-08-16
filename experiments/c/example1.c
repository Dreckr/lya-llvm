#include <stdio.h>

int main() {
    int m, n, s;

    scanf("%d %d", &m, &n);

    s = 0;

    while (m <= n) {
        s += m * n;

        printf("%d %d\n", m, s);

        m += 1;
    }

    return 0;
}
