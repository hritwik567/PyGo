package main

func main() {
	var a [3][3]int
	var b [3][3]int
	var res [3][3]int

	c := 0
	for i := 0; i < 3; i++ {
		for j := 0; j < 3; j++ {
			a[i][j] = c
      c++
      printf("c %d a[i][j] %d\n",c,a[i][j])
		}
	}

  // for i := 0; i < 3; i++ {
	// 	for j := 0; j < 3; j++ {
	// 		printf("%d ", a[i][j])
	// 	}
	// 	printf("\n")
	// }


	// for i := 0; i < 3; i++ {
	// 	for j := 0; j < 3; j++ {
	// 		b[i][j] = c
  //     c++
	// 	}
	// }
  //
  // for i := 0; i < 3; i++ {
	// 	for j := 0; j < 3; j++ {
	// 		printf("%d ", b[i][j])
	// 	}
	// 	printf("\n")
	// }
  //
	// for i := 0; i < 3; i++ {
	// 	for j := 0; j < 3; j++ {
	// 		c = 0
	// 		for k := 0; k < 3; k++ {
	// 			d := a[i][k]
	// 			e := b[k][j]
	// 			c = c + d*e
	// 		}
	// 		res[i][j] = c
	// 	}
	// }
  //
	// for i := 0; i < 3; i++ {
	// 	for j := 0; j < 3; j++ {
	// 		printf("%d ", res[i][j])
	// 	}
	// 	printf("\n")
	// }
}
