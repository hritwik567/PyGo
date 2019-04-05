package main

import "fmt"

func main() {

  var factorials [11]int

  for iter := 0; iter < 11; iter++ {

    if iter == 0 {
      factorials[iter] = 1
      continue
    }

    factorials[iter] = factorials[iter-1] * iter

  }
}
