package main

import "fmt"

func fb(n int) int;

func fa(n int) int {
  if n==1 || n==0 {
    return 1
  }
  return n + fb(n-1)
}


func fb(n int) int {
	if n==1 || n==0 {
    return 1
  }
  return n + fa(n-1)
}

func main() {
	v := fb(5)
}
