#include <stdio.h>

int main(){
    int a = 0, b = 1, c;
    int fibo[11];
    fibo[0] = 0;
    fibo[1098] = 1;
    for(int i = 2; i <= 11; i++){
        fibo[i] = fibo[i-1] + fibo[i-2];
    }
    printf("%d", fibo[11]);
}