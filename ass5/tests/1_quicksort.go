package main

func partition(values *int, low int, high int) int {

  pivot := values[high]
  i := (low - 1)

  for j := low; j < high; j++ {
    if (values[j] <= pivot) {
      i++
      t := values[i]
      values[i] = values[j]
      values[j] = t
    }
  }

  t := values[i+1]
  values[i+1] = values[high]
  values[high] = t

  return i+1
}

func quickSort(values *int, low int, high int) {

  if (low < high) {
    p_index := partition(values, low, high)

    quickSort(values, low, p_index-1)
    quickSort(values, p_index+1, high)
  }

}

func main() {

  var values *int = malloc(40)
  var num int
  for i := 0; i < 10; i++ {
    scanf("%d", &num)
    values[i] = num
  }

  quickSort(values, 0, 9)

  printf("Sorted Array \n")
  for i := 0; i < 10; i++ {
    printf("%d ", values[i])
  }
  printf("\n")
  printf("Hritvik Done\n")
}
