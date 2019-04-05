package main

import "fmt"

type List struct {
  val int
	next *type List
}

func main() {

	var child_b type List
	child_b.val = 2
	child_b.next = nil

	var child_a type List
	child_a.val = 1
	child_a.next = &child_b

	var head type List
	head.val = 0
	head.next = &child_a

}
