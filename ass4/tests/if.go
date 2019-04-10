package main

import "fmt"

func main() {
	var can_vote = 0
	var age_threshold = 18
	var age = 23
	if (age > age_threshold) {
		can_vote = 1
	}

  i := 1
  j := 2

  equal := false

  if i > j {
    j++
  } else if i < j {
    j--
  } else {
    equal = true
  }

  s := "Are they Equal?"
  if equal {
    s = "Yes, they are"
  } else {
    s = "No, they're not"
  }
}
