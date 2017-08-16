#include <stdio.h>
#include <stdbool.h>

int main() {
    int n1, n2, i, j;
    bool flag;

    printf("Enter 2 numbers (intervals) separated by space: \n");

    scanf("%d %d", &n1, &n2);

    printf("Prime numbers between %d and %d are:\n", n1, n2);

    for (i = n1; i <= n2; i++) {
        flag = true;

        for (j = 2; j <= i / 2; j++) {
            if (i % j == 0) {
                flag = false;

                break;
            }
        }

        if (flag) {
            printf("%d\n", i);
        }
    }

    return 0;
}
