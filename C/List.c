#include <stdio.h>
#include <stdlib.h>
#include "List.h"

struct Node
{
    Type* a;
    struct Node* next;
};

typedef struct Node* node;

struct ListArray
{
    int size;
    struct Node* first, *last;
};

List List_create()
{
    List l = calloc(1, sizeof(struct ListArray));
	l-> size = 0;
    return l;
}

int List_size(List l)
{
	return l->size;
}

void List_destroy(List l)
{
	if(l->size==0)
		free(l);
	else
	{
		int i;
		node current = l->first;
		if(l->first==l->last)
		{
			free(l->first);
			free(l);
		}
		else
			for(i=0;i<l->size;i++)
			{
				l->first = current->next;
				free(current);
				current = l->first;
			}
		free(l);
	}
}

void List_add(List l, Type b)
{
    node c = calloc(1, sizeof(struct Node));
	c->a = b;
	if(l->size == 0)
		l->first = l->last = c;
	else
	{
		l->last->next = c;
		l->last = c;
	}
	l->size++;
}

Type List_get(List l, int p)
{
	if(l->size == 0 || (l->size-1) < p)
		return -1;
	node current = l->first;
	for(int i = 0; i < p; i++)
		current = current->next;
	return current->a;
}

Type List_set(List l, Type b, int p)
{
	if(l->size == 0 || (l->size-1) < p)
		return -1;
	node current = l->first;
	for(int i = 0; i < p; i++)
		current = current->next;
	current->a = b;
	return b;
}

char* toString(List l)
{
	if(l->size == 0)
		return "[]";
	node current = l->first;
	while(current != l->last)
	{
		
	}
}

/*Type List_remove(List l , int p)
{
	if(p>=(l->size*l->asize))
		return -1;
	if(p<0)
		return -1;
	int i, i2;
	node current = l->first;
	i = p/l->asize;
	for(i2=0; i2<i; i2++)
		current = current->next;
	i = p%l->asize;
	for(i2=0; i2!=i; i2++);
	Type t = current->a[i2];
	if(i2%l->asize==l->asize-1)
		current->a[i2] = 0;
	else
		for(;i2%l->asize!=l->asize-1;i2++)
			current->a[i2] = current->a[i2+1];
	current->a[i2] = 0;
	return t;
}

void delete_node(List l, Type b)
{
	node current, prev;
	current = l->first;
	int i, i2;
	for(i=0;i<l->size;i++)
	{
		for(i2=0;i2<l->asize && current->a[i2]==0;i2++);
		if(i2==l->asize)
		{
			if(current==l->first)
			{
				l->first = l->first->next;
				l->size--;
			}
			else
			{
				prev->next = current->next;
				l->size--;
			}
		}
		prev = current;
		current = current->next;
	}
}

void List_pack(List l)
{
	node current;
	Type tem;
	int i, i2, i3, b, c=0, b2=0;
	delete_node(l);
	if(l->size==0);
	else
	{
		current = l->first;
		for(i=0;i<l->size;i++)
		{
			b=0;
			for(i2=0;i2<l->asize;i2++)
			{
				if(current->a[i2]==0)
				{
					for(i3=i2+1;i3<l->asize && current->a[i3]==0;i3++);
					if(i3!=l->asize)
					{
						b=1;
					}
				}
				if(current->a[i2]==0 && b==1)
				{
					List_remove(l, ((i+1)*l->asize-(l->asize-i2)));
					i2--;
					b=0;
				}
			}
				current = current->next;
		}
		current = l->first;
		for(i=0;i<l->size;i++)
		{
			for(i2=0;i2<l->asize && current->a[i2]!=0;i2++);
			if(i2!=l->asize)
			{
				tem = List_remove(l, l->asize*(i+1));
				if(tem!=-1)
				{
					current->a[i2] = tem;
					delete_node(l);
					i--;
				}
				else
					current->a[i2] = 0;
			}
			else
				current = current->next;
		}
	}
}*/