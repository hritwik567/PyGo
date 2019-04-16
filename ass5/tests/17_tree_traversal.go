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
	
	// printf("Insert node\n")
	// printf("1\n")
	if head == nil {
		return new_node(val)
	}

	temp := *head

	// printf("2\n")
	if val < temp.v {
		// printf("3.a\n")
		head[0].l = insert_node(temp.l, val)
	} else if val > temp.v {
		// printf("3.b\n")
		head[0].r = insert_node(temp.r, val)
	}

	head[0] = temp
	// printf("4\n")
	return head;
}

func search(root *type node, key int) *type node {
	if root == nil {
		return root
	}

	printf("Encountered %d\n", root[0].v);
	if root[0].v == key {
		return root
	}

	if root[0].v < key {
		printf("Going Right\n");
		return search(root[0].r, key)
	}

	if root[0].v > key {
		printf("Going Left\n");
		return search(root[0].l, key)
	}
}

func main(){
	head := new_node(3)
	head = insert_node(head, 5)
	// printf("head: %lx\n", head);
	// printf("head val: %lx\n", head[0].v);
	// printf("head left: %lx\n", head[0].l);
	// printf("head right: %lx\n", head[0].r);
	
	head = insert_node(head, 2)
	head = insert_node(head, 8)
	head = insert_node(head, 1)


	printf("head val: %lx\n", head[0].v);
	printf("head left: %lx\n", head[0].l);
	printf("head right: %lx\n", head[0].r);

	var t3 type node = head[0]
	printf("head val: %lx\n", t3.v);
	printf("head val: %lx\n", t3.l);
	printf("head val: %lx\n", t3.r);
	t4 := t3.r
	 
	printf("head val: %lx\n", t4[0].v);
	printf("head left: %lx\n", t4[0].l);
	printf("head right: %lx\n", t4[0].r);
	// 
	// // t3 = t4[0]
	// // printf("head val t1: %lx\n", t3.v);
	// 
	
	
	// printf("head val: %lx\n", head[0].v);
	// printf("head left: %lx\n", head[0].l);
	// printf("head right: %lx\n", head[0].r);

	// t1 := head[0].r
	// printf("head: %lx\n", head);
	// printf("head val: %lx\n", head[0].v);
	// printf("head left: %lx\n", head[0].l);
	// printf("head right right: %lx\n", t1[0].v);

	lookup := search(head, 2)
	if lookup == nil {
		printf("Coulnd't find 5\n");
	} else{
		temp := lookup[0]
		printf("Val: %d\n", lookup[0].v)
	}
}
