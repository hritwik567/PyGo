package main

import (
	"fmt"
)

func main() {
course := "compiler"

fmt.Printf("This is for a %s\n", course)
fmt.Printf(`This "is" for a \n`);

var sum int = 0

for i := 0; i < 10; i++ {
	sum += i
}

if sum < 8 {
	sum /= 2
} else {
	sum %= 2
}

}
