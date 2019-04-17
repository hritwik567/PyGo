package main

func main() {
  var a = 1
  a = 2
  b := 2 + a

  var x float32 = 2 // Erraneous
  y := x + 1.0 // Erraneous

  var s string = "type checking"
  s = 1 + 2 // Erraneous
  var d float32
  d = a // Erraneous

}
