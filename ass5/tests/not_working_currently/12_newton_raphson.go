package main

var EPSILON = 0.001

func abs(val float32) float32 {
  if val < 0 {
    return -1.0 * val
  }
  return val
}

func Func(val float32) float32 {
  result := val*val*val - val*val + 2.0
  return result
}

func derivFunc(val float32) float32 {
  result := 3*val*val - 2*val
  return result
}

func newtonRaphson(val float32) float32 {

  growth := Func(val) / derivFunc(val)
  root := val

  for abs(val) >= EPSILON {
    growth = Func(val) / derivFunc(val)
    root = root - growth
  }

  return root
}

func main() {

  val := 20.0
  root := newtonRaphson(val)
  //printf("The root is: %d\n", root)

}
