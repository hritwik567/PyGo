package main

func is_even(num int) bool {
  if num == 0 {
    return true
  }
  return is_odd(num-1)
}

func is_odd(num int) bool {
  if num == 0 {
    return false
  }
  return is_even(num-1)
}

func main() {
  var val int
  printf("Give a positive integer: ")
  scanf("%d", &val)

  result := is_even(val)
  switch result {
    case false:
      printf("%d is odd", result)
    default:
      printf("%d is even", result)
  }
}
