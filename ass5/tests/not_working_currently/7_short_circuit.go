package main

func check(val bool) bool {
  //printf("here")
  return val
}

func main() {
  // should NOT print
  a := true || check(false)

  // should print
  b := false || check(true)

  // should NOT print
  c := false && check(true)

  // should print
  d := true && check(false)
}
