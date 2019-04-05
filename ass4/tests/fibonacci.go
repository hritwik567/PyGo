package main

import "fmt"

func main() {

  var fibonacci [11]int

  for iter := 0; iter < 11; iter++ {

    if iter == 0 || iter == 1 {
      fibonacci[iter] = 1
      continue
    }

    fibonacci[iter] = fibonacci[iter-1] + fibonacci[iter-2]

  }
}
