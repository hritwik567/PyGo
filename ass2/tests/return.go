package main

import "fmt"

// func foo1(a int, b int) {
// 	fmt.Println(a, b);
// }
//
// func foo2(a int, b int) () {
// 	fmt.Println(a, b);
// }
//
// func foo3(a int, b int) int {
// 	fmt.Println(a, b);
// 	return a
// }
//
// func foo4(a int, b int) (int) {
// 	fmt.Println(a, b);
// 	return a
// }
//
// func foo5(a int, b int) (a int) {
// 	fmt.Println(a, b);
// 	return a
// }

func foo6(a int, b int) (int, int) {
	fmt.Println(a, b);
	return a,b
}


func main() {
	fmt.Println("vim-go")

}
