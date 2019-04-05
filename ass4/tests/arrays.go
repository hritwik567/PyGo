package main

import "fmt"

func main() {
  var c [3]float32
  c[0] = 1 + 3
  var a = 2.01
  c[2] = a
  c[1] = a * 10.0

  var e [2][3][4]int
  e[0][1][2] = 3

  var arr [5][5]bool
  arr[0][2] = true
  arr[0][3] = !arr[0][2]
}
