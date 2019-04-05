package main

import "fmt"

type Tree struct {
  val int
  left *type Tree
	right *type Tree
}

func main() {

	var left_child type Tree
	left_child.val = 0
	left_child.left = nil
	left_child.right = nil

	var right_child type Tree
	right_child.val = 2
	right_child.left = nil
	right_child.right = nil

	var root type Tree
	root.val = 1
	root.left = &left_child
	root.right = &right_child

}
