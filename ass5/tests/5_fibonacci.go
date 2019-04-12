package main

func main() {

  var size int
  printf("Till what index do you want the fibonacci series: ")
  scanf("%d", &size)

  var fibonacci [size]int

  for i := 0; i < size; i++ {

    if i == 0 || i == 1 {
      fibonacci[i] = 1
      continue
    }

    fibonacci[i] = fibonacci[i-1] + fibonacci[i-2]
  }

  printf("Fibonacci Series\n")
  for i := 0; i < size; i++ {
    printf("%d ")
  }
  printf("\n")
}
