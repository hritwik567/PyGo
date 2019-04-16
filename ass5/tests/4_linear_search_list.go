package main

type ll struct {
	a    int
	next *type ll
}

func main() {
	var a1 type ll;
	var a2 type ll;
	var a3 type ll;
	var a4 type ll;

	a1.a = 1
	a2.a = 2
	a3.a = 3
	a4.a = 4

	a1.next = &a2
	a2.next = &a3
	a3.next = &a4
	a4.next = nil

	head := &a1

	found := 0
	for {
		if head == nil {
			break
		}
    temp := *head
		if temp.a == 3 {
			found = 1
			break
		}
		head = temp.next
	}

	if found == 1 {
		printf("Found\n")
	} else {
		printf("Not found\n")
	}
}
