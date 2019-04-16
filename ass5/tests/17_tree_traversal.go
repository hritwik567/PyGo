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
	
	printf("Insert node\n")
	printf("1\n")
	if head == nil {
		return new_node(val)
	}

	temp := *head

	printf("2\n")
	if val < temp.v {
		printf("3.a\n")
		temp.l = insert_node(temp.l, val)
	} else if val > temp.v {
		printf("3.b\n")
		temp.r = insert_node(temp.r, val)
	}

	head[0] = temp
	printf("4\n")
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
	printf("head: %lx\n", head);
	printf("head val: %lx\n", head[0].v);
	printf("head left: %lx\n", head[0].l);
	printf("head right: %lx\n", head[0].r);
	
	head = insert_node(head, 2)


	printf("head: %lx\n", head);
	printf("head val: %lx\n", head[0].v);
	printf("head left: %lx\n", head[0].l);
	printf("head right: %lx\n", head[0].r);

	// t1 := *head
	// t2 := t1.l
	// t1 = *t2
	// printf("head val: %lx\n", t2.v);
	
	head = insert_node(head, 8)
	head = insert_node(head, 1)

	t1 := head[0].r
	// printf("head: %lx\n", head);
	// printf("head val: %lx\n", head[0].v);
	// printf("head left: %lx\n", head[0].l);
	printf("head right right: %lx\n", t1[0].v);

	lookup := search(head, 2)
	if lookup == nil {
		printf("Coulnd't find 5\n");
	} else{
		temp := *lookup
		printf("Val: \n", temp.v)
	}
}
