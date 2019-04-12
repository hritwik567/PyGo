package main

func binarySearch(values []int, l, r, key int) int {

  if (r >= l) {
    mid := l + (r - l) / 2

    if (values[mid] == key) {
      return mid
    }

    if (values[mid] > key) {
      return binarySearch(values, l, mid-1, key)
    }

    return binarySearch(values, mid+1, r, key)
  }

  return -1
}

func main() {

  var size int
  printf("Give me the size of the array: ")
  scanf("%d", &size)

  var key int
  printf("Give me the key to search for: ")
  scanf("%d", &key)

  var values [size]int
  for i := 0; i < size; i++ {
    var num int
    scanf("%d", &num)
    values[i] = num
  }

  result := binarySearch(values, 0, size-1, key)

  switch result {
    case -1:
      printf("Element is not present in array")
    default:
      printf("Element is present at index %d", result)
  }
}
