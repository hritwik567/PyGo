package main

func swap(values []int, a int, b int) {
  t := values[a]
  values[a] = values[b]
  values[b] = t
}

func partition(values []int, low int, high int) int {

  pivot := values[high]
  i := (low - 1)

  for j := low; j < high; j++ {
    if (values[j] <= pivot)
    {
      i++
      swap(values, i, j)
    }
  }

  swap(values, i+1, high)
  return i+1
}

func quickSort(values []int, low int, high int) {

  if (low < high) {
    p_index := partition(values, low, high)

    quickSort(values, low, p_index-1)
    quickSort(values, p_index+1, high)
  }

}

func main() {

  var size int
  printf("Give me the size of the array: ")
  scanf("%d", &size)

  var values [size]int
  for i := 0; i < size; i++ {
    var num int
    scanf("%d", &num)
    values[i] = num
  }

  quickSort(values, 0, size-1)

  printf("Sorted Array \n")
  for i := 0; i < size; i++ {
    printf("%d ", values[i])
  }
  printf("\n")

}
