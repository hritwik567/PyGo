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


func main() {
	// var a float32 = 2
	// var b = 2
	// b = foo(b)
	// var c [3]float32
	// c[0] = 1 + 3
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
	var d [3]string
	d[0] = "Hritvik"
	d[1] = "Hritvik"
	d[2] = "Hritvik"
	// for {
	// 	var x =3
	// 	continue
	// 	break
	// }
	// var t = true
	// var a = 4
	// var b = 5
	// if a < b {
	// 	var x = 3
	// } else if true {
	// 		var x = 5
	// } else {
	// 		var x = 4
	// }


}
