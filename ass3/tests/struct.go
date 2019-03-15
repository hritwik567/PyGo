package main

import "fmt"

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

	var d type T
	d.a.c[2] = 4
	d.c[0] = 3

}
