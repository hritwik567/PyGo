package main

import "fmt"

func fact(n int) int {
  if n==1 || n==0 {
    return 1
  }
    return n*fact(n-1)
}

type Point struct {
  x int
  y int
  dist float32
}

func getSums() int {

  // Find all factorials below 1000

  var arr [10]int

  var iter int
  for iter = 1; iter <= 10; iter++ {
    if (fact(iter) > 1000) {
      break
    }
    arr[iter-1] = iter
  }

  // Get Words for the integers

  for i := 0; i < iter; i++ {
    switch arr[i] {
      case 1,3,5,7,9:
        return i*(i+1)/2
      case 2,4,6,8:
        return i*i/2
    }
  }
}

func calc_dist(a,b type Point) float32 {
  var x float32 = typecast float32(a.x) - typecast float32(b.x)
  var y float32 = typecast float32(a.y) - typecast float32(b.y)
  return x*x + y*y
}

func main() {
  var final_ans int = getSums()

  var new_point type Point
  new_point.x = 3
  new_point.y = 4

  var new_point2 type Point
  new_point2.x = 35
  new_point2.y = 45

  var dist = calc_dist(new_point, new_point2)
}
