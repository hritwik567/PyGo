package main

func main() {
  var a = fopen("temp1.txt", "w+")
  fprintf(a, "Hritvik taneja\n")
  fclose(a)

  var b = fopen("temp2.txt", "w+")
  fprintf(b, "2\n")
  fclose(b)

  var c int
  var d = fopen("temp2.txt", "r")
  fscanf(d, "%d", &c)
  fclose(d)

  printf("%d\n", c)

  printf("Hritvik Done\n")

}
