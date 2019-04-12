package main

var size = 10
var values [10]int

func swap(a int, b int) {
  t := values[a]
  values[a] = values[b]
  values[b] = t
}

func partition(low int, high int) int {

  pivot := values[high]
  i := (low - 1)

  for j := low; j < high; j++ {
    if (values[j] <= pivot)
    {
      i++
      swap(i, j)
    }
  }

  swap(i+1, high)
  return i+1
}

func quickSort(low int, high int) {

  if (low < high) {
    p_index := partition(low, high)

    quickSort(low, p_index-1)
    quickSort(p_index+1, high)
  }

}

func main() {

  for i := 0; i < size; i++ {
    var num int
    //scanf("%d", &num)
    values[i] = num
  }

  quickSort(0, size-1)

  //printf("Sorted Array \n")
  //for i := 0; i < size; i++ {
  //  printf("%d ", values[i])
  //}
  //printf("\n")

}
