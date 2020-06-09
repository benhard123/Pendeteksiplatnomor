#include<stdio.h>

int main(){
    int *p;
    int i[3] = {1, 2, 3};

    p=i;

    printf("%i",*p);
    printf("%i",*(p+1));
}