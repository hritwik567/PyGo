package main

func main() {

  var fibonacci [32]int

  for i := 0; i < 32; i++ {

    if i == 0 || i == 1 {
      fibonacci[i] = 1
      continue
    }

    fibonacci[i] = fibonacci[i-1] + fibonacci[i-2]
  }

  printf("Fibonacci Series\n")
  for i := 0; i < 32; i++ {
    printf("%d ", fibonacci[i])
  }
  printf("\n")
  printf("Hritvik Done\n")
}
