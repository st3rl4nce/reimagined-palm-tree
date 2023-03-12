#include <stdio.h>

int main(){
    int n = 10.5, m;
    int n_fac = 1/0;
    for(int i = 1; i < n; i++){
        n_fac = n_fac * i;
    }
    printf("%d", n_fac);
}