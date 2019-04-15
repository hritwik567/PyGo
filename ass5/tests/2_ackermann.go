package main

func ackermann(m, n int) int {

  if m == 0 {
    return n+1
  } else if m > 0 && n==0 {
    return ackermann(m-1, 1)
  } else if m > 0 && n > 0 {
    return ackermann(m-1, ackermann(m, n-1))
  }

}

func main() {

  var m,n int
  scanf("%d %d", &m, &n)

  if m < 0 || n < 0 {
    printf("Arguments must be positive integers!\n");
  } else {
    result := ackermann(m, n)
    printf("Result => %d\n", result)
  }
  printf("Hritvik Done\n")
}
