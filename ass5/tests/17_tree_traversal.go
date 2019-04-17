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

// func inorder(root *type node) void;

func inorder(root *type node) int {
	if root == nil {
		return 0
	}

	retval := inorder(root[0].l)

	printf("%d, ", root[0].v)
	
	retval = inorder(root[0].r)

	return 0
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

	if root[0].v == key {
		return root
	}

	if root[0].v < key {
		return search(root[0].r, key)
	}

	if root[0].v > key {
		return search(root[0].l, key)
	}
}

func main(){
	head := new_node(3)
	head = insert_node(head, 5)
	head = insert_node(head, 2)
	head = insert_node(head, 8)
	head = insert_node(head, 1)
	head = insert_node(head, 22)
	head = insert_node(head, 23)
	head = insert_node(head, 84)
	head = insert_node(head, 12)
	head = insert_node(head, 85)
	head = insert_node(head, 13)



	printf("Inorder Traversal\n")
	inorder(head)
	printf("\n")
  printf("Hritvik Done")
}
