package main

func long_add(a,b,c,d,e,f,g,h int) int {
  return a+b+c+d+e+f+g+h
}

func main() {
  result := long_add(1,2,3,4,5,6,7,8)
  printf("Result -> %d", result)
}
