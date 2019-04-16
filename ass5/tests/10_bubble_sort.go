package main

func main() {
	var b [10]int
	for i := 0; i < 10; i++ {
		d := 0
		scanf("%d", &d)
		b[i] = d
	}

	for i := 0; i < 9; i++ {
		for j := 0; j < 9; j++ {
			if b[j] > b[j+1] {
				c := b[j]
				b[j] = b[j+1]
				b[j+1] = c
			}
		}
	}

  for i := 0; i < 10; i++ {
	   printf("%d ", b[i])
  }
	printf("\n")
  printf("Hritvik Done\n")
}
