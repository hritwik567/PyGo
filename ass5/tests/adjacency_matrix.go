package main

type kk struct {
	a int
	b * type kk
}

func main() {
	var str [10]*type kk
	for i := 0; i < 10; i++ {
		str[i] = malloc(8)
		ptr := str[i]
		for j := 0; j < 10; j++ {
			ptr.a = 10 + i*10 + j
			ptr.b = malloc(8)
			ptr = ptr.b
		}
	}

	for i := 0; i < 10; i++ {
		ptr := str[i]
		for j := 0; j < 10; j++ {
			printf("%d\n", ptr.a)
			ptr = ptr.b
		}
	}
}
