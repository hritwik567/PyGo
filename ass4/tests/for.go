package main

import "fmt"

func main() {
  sum := 0
  for i := 1; i <= 10; i++ {
    sum = sum + i
    continue
    sum = sum - 1
    break
    sum++
  }

  i := 10
  for i > 0 {
    sum = sum - i
    i--
    continue
    sum = sum + 1
    break
    sum--
  }

  for {
    sum++
  }
}
