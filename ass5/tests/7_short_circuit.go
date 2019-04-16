package main

func check() int {
  printf("\t Check function executed\n")
  return 1
}

func main() {
  a := 1

  if a == 1 || check() == 1 {
    printf("Should not execute check function\n")
  }

  if a > 1 || check() == 1 {
    printf("Should execute check function\n")
  }

  if a > 1 && check() == 1 {
    printf("Should not be here\n")
  } else {
    printf("Should not execute check function\n")
  }

  if a == 1 && check() == 1 {
    printf("Should execute check function\n")
  }

  printf("Hritvik Done\n")

}
