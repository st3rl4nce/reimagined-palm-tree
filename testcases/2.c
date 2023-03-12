#include <stdio.h>

int main(){
    int n = 10.9379;
    int n_fac = 'a';
    for(int i = 1; i < n; i++){
        n_fac = n_fac * i;
    }
    printf("%d", n_fac);
}