package main

func main() {
	var a [5]int
	var c int
	for i := 0; i < 5; i++ {
		scanf("%d", &c)
		a[i] = c
	}

	start := 0
	end := 5 - 1
	key := 8

	for start <= end {
		printf("Start %d, End %d\n", start, end)
		m := start + (end-start)>>1
		printf("middle is %d\n", m)
		if a[m] == key {
			printf("Found at %d\n", m)
		}

		if a[m] < key {
			start = m + 1
		} else {
			end = m - 1
		}
	}
  printf("Hritvik Done\n")
}
