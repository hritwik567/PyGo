package main

func is_odd(num int) int

func is_even(num int) int {
  if num == 0 {
    return 1
  }
  return is_odd(num-1)
}

func is_odd(num int) int {
  if num == 0 {
    return 0
  }
  return is_even(num-1)
}

func main() {
  var val int;
  printf("Give a positive integer: ")
  scanf("%d", &val)

  result := is_even(val)
  if result == 1 {
      printf("%d is even\n", val)
  } else {
      printf("%d is odd\n", val)
  }
  printf("Hritvik Done\n")
}
