package main

type List struct {
  	val int
  	next *type List
}

func foo(a type List) int {
	c := a.val
	return c
}

func node(a type List) *type List {
  var b *type List = malloc(8)
  b[0].val = a.val + 1
  b[0].next = nil
  return b
}

func main() {
  var head type List
  head.val = 1
  head.next = nil
  b := foo(head)
  printf("%d\n", b)

  var root *type List
  root = node(head)
  printf("%d\n", root[0].val)

  printf("Hritvik Done\n")
}
