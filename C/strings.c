#include <stdlib.h>
#include <stdio.h>

char* input()
{
    char input[1024];
    gets(input);
    int i = 0;
    for(; input[i] != '\0'; i++);
    char* s = malloc(i);
    for(int i2 = 0; i2 <= i; i2++)
        s[i2] = input[i2];
    return s;
}

int length(char* string)
{
	int i = 0;
	for(;string[i] != '\0'; i++);
	return i;
}

char* concat(char* a, char* b)
{
    int la = length(a);
    int lb = length(b);
    char* string = malloc(la + lb + 1);
    int i = 0;
    for(; i < la; i++)
        string[i] = a[i];
    for(; i < la+lb+1; i++)
        string[i] = b[i-la];
    return string;
}

int main()
{
	char* s1 = input();
    char* s2 = input();
	printf("s1 = %s ... length = %d\n", s1, length(s1));
    printf("s2 = %s ... length = %d\n", s2, length(s2));
    char* s12 = concat(s1, s2);
    char* s21 = concat(s2, s1);
    printf("s1 + s2 = %s ... length = %d\n", s12, length(s12));
    printf("s2 + s1 = %s ... length = %d\n", s21, length(s21));
}