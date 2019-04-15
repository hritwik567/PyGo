package main

import "fmt"
//
// func foo(a int) int {
// 		return 1
// }
//
// func fact(n int) int {
//   if n==1 || n==0 {
//     return 1
//   }
//   return n*fact(n-1)
// }

type P struct {
	a int
	b float64
	c [3]int
	d float32
	e int
	f float32
}

type T struct {
	b float64
	c [3]int
	a type P
	d float32
	e int
	f float32
}

type List struct {
  	val int
  	left *type List
	right *type List
}

// func foo(a type List) int {
// 	c := a.val
// 	return c
// }

func main() {
	// var a float32 = 2
	// var head type List
	// head.val = 1
	// head.left = nil
	// head.right = nil
	// b := foo(head)
	var b = 2
	var c = 3
	// var l *int
	// l = &b;
	// *l = 2
	// var c [3]int
	// c[0] = *l + foo(foo(1,2), c[0])

	// var a = fopen("abc", "w+")
	// fprintf(a, "Hritvik taneja\n")
	scanf("%d", &b)
	scanf("%d", &c)
	printf("Hritvik, taneja %d\n", b)
	printf("Hritvik, taneja %d\n", c)

	//
	// {
	// 	var a = 2.01
	// 	c[2] = a
	// }
	// c[1] = a
	// var d type T
	// d.a.c[2] = 4
	// d.c[0] = 3
	// var e [2][3][4]int
	// e[0][1][2] = 3
	// var l = true
	// var k = false
	// var t = l||k
	// var d [3]string
	// d[0] = "Hritvik"
	// d[1] = "Hritvik"
	// d[2] = "Hritvik"
	// ll := foo(1,2)
	// l := 3;
	// m := 4;
	// n := 5;
	// r := l + 1
	// o := l*(m + m*(n + n*(l  + l*m*n)));
	// k := l*m + m*n + n*l  + l*m*n;
	// i := l*l + foo(1,2)*l
	// var head type List
	// head.val = 1
	// head.left = nil
	// head.right = nil
	// var head1 type List
	// head1.val = 1
	// head1.left = &head
	// head1.right = nil
	// for {
	// 	var x =3
	// 	continue
	// 	break
	// }
	// var t = true
	// var a = 4
	// var b = 5
	// var x = 2
	//
	// if a < b || a == 4 {
	// 	printf("here1\n")
	// 	x = 3
	// } else if true {
	// 	printf("here2\n")
	// 		x = 5
	// } else {
	// 	printf("here3\n")
	// 		x = 4
	// }
	// printf("%d\n", x)


}
