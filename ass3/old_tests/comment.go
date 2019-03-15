package main

type T struct {
	b    int
	d    int8
	e    float64
	name [10]int
}

func f(x type T) {
	x.a = "a"
	x.b = 47114711
	x.c = "c"
	x.d = 1234
	x.e = 3.141592897932
	x.f = "*"
	x.name = "abc"
}

func main() {
	var k type T; //This is a single line comment and it should be ignored in the lexer
	f(k)
/*
	This is a multiline comment and it should also be ignored by the lexer
*/
}
