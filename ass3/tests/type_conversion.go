package main

import "fmt"

func main(){
	var a float32 =4
	var b uint8 = 2
	var c int = 24
	var d uint8 = typecast uint8(a)
	var e float32 = typecast float32(b)
	var f float32 = typecast float32(c)
	var g uint8 = typecast uint8(a)
	var h uint8 = typecast uint8(c)
	var i int = typecast uint8(a)
	var j int = typecast uint8(b)
}
