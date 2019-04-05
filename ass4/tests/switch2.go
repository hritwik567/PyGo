package main

import "fmt"

func main() int {
  var number int = 1
  unit_digit := number % 10
  var is_even bool
  switch number {
    case 0,2,4,6,8:
      is_even = true
    default:
      return -1
    case 1,3,5,7,9:
      is_even = false
  }

  switch {
    default:
      return -1
    case is_even && number < 100:
      return number
    case !is_even && number < 100, !is_even && number >= 100:
      return (number+1)%100
    case is_even && number >= 100:
      return number % 100
  }
}
