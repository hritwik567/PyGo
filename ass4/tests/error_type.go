// Please uncomment and comment 
// different parts of code to see different error handling

package main

func foo(a int, b float32) int;


// prototype and definition parameters type mismatch
func foo(c int, d int) int {
	return 4
}


func main(){
	// var b = a // gives error of undeclared identifier
	var c int = 3
	var d float32 = 5.1
	// var e = c + d // type mismatch
}
