package main

import "fmt"

func main() {
	var sum = 0
	for i := sum; i < sum + 10; i=i+1 {
		sum = sum + i
		if(sum > 100){
			break;
		}
		if (i == 69){
			continue
		}
	}
}
