package main

type node struct{
	v int
	l *type node
	r *type node
}

func new_node(val int) *type node {
	var newnode *type node = malloc(12)
	newnode[0].v = val
	newnode[0].l = nil
	newnode[0].r = nil
	return newnode
}

func insert_node(head *type node, val int) *type node {

	if head == nil {
		return new_node(val)
	}

	temp := *head

	if val < temp.v {
		temp.l = insert_node(temp.l, val)
	} else if val > temp.v {
		temp.r = insert_node(temp.r, val)
	}

	*head = temp
	return head;
}

func search(root *type node, key int) *type node {
	if root == nil {
		return root
	}

	temp := *root
	printf("Encountered %d\n", temp.v);
	if temp.v == key {
		return root
	}

	if temp.v < key {
		printf("Going Right\n");
		return search(temp.r, key)
	}

	if temp.v > key {
		printf("Going Left\n");
		return search(temp.l, key)
	}
}

func main(){
	head := new_node(3)
	head = insert_node(head, 5)
	head = insert_node(head, 2)
	head = insert_node(head, 8)
	head = insert_node(head, 1)

	lookup := search(head, 5)
	if lookup == nil {
		printf("Coulnd't find 5\n");
	} else{
		temp := *lookup
		printf("Val: \n", temp.v)
	}
}
