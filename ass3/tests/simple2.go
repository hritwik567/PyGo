package main

import "fmt"

func main() {
  var a, b, c int = 1, 2, 3
  var x, y, z = 1.1, 2.2, 3.3

  num := a * b / (b + c - a)
  frac := z / y * (x + z) * y / z

  var flag = false
  var f bool = true
  var d = f == flag
}
