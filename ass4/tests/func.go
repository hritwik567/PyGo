package main

import "fmt"


func foo(a int) int {
	var c = a +  2; 	
	return c
}


func main() {
	var c int = 5;
	var d float32 = 92.2;
	var a int = foo(c);
}
