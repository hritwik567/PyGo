package main

func Func(val int) int {
  result := val*val
  return result
}

func derivFunc(val int) int {
  result := 2*val
  return result
}

func newtonRaphson(val int) int {

  growth := val >> 1

  for abs(growth) >= 1 {
    growth = val >> 1
    val = val - growth
    if growth == 0 {
      break
    }
  }

  return val
}

func main() {

  val := 200
  root := newtonRaphson(val)
  printf("The root is: %d\n", root)

}
