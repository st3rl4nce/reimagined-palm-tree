#include <stdio.h>

int count(int n);

// main funciton
int main(){
    int a=10;
    int f = 'a';
    char b;
    float d='j';
    b=a++;
    a=d;
    a = 5/0;
    int arr[10];
    arr[10] = 'k';
    count('b');
    int ret = count(1234567890);
    printf("%d",count(1234567890));
    return 0;
}

int count(int n){
    int i=0.5;
    int arr[10];
    arr[10]=5;
    while(n>0){
        i++;
        n=n/10;
    }
    return 'c';
}


