#ifndef LIST_H_
#define LIST_H_


typedef struct ListArray* List;
typedef void* Type;

List List_create();
void List_destroy(List);
int List_size(List);
void List_add(List, Type);

Type List_get(List, int);
Type List_set(List, Type, int);
Type List_remove(List, int);

void List_insert(List, Type, int);
void List_pack(List);


#endif /* LIST_H_ */