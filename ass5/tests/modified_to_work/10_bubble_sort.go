package main

var size = 10
var values [10]int

func swap(a,b int) {
  t := values[a]
  values[a] = values[b]
  values[b] = t
}

func bubbleSort(size int) {

  for i := 0; i < size-1; i++ {
    for j := 0; j < size-i-1; j++ {
      swap(values, i, j)
    }
  }

}

func main() {

  for i := 0; i < size; i++ {
    var num int
    //scanf("%d", &num)
    values[i] = num
  }

  bubbleSort(values, size)

  //printf("Sorted Array \n")
  //for i := 0; i < size; i++ {
  //  printf("%d ", values[i])
  //}
  //printf("\n")

}
