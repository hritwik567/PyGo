package main

var size = 10
var values [10]int

func binarySearch(l, r, key int) int {

  if (r >= l) {
    mid := l + (r - l) / 2

    if (values[mid] == key) {
      return mid
    }

    if (values[mid] > key) {
      return binarySearch(l, mid-1, key)
    }

    return binarySearch(mid+1, r, key)
  }

  return -1
}

func main() {

  var key int
  //printf("Give me the key to search for: ")
  //scanf("%d", &key)

  for i := 0; i < size; i++ {
    var num int
    //scanf("%d", &num)
    values[i] = num
  }

  result := binarySearch(0, size-1, key)

  switch result {
    case -1:
      return
      //printf("Element is not present in array")
    default:
      return
      //printf("Element is present at index %d", result)
  }
}
