package main

import "fmt"

func foo(a int) int {
		var t = a
}

type T struct {
	a int
	b float64
	c [3]int
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
	// d.c[0] = 3
	var e [2][3][4]int
	e[0][1][1] = 3
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
