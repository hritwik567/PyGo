package main

import "fmt"

func main() {
	var can_vote = 0
	var age_threshold = 18
	var age = 23
	if (age > age_threshold){
		can_vote = 1;
	} else{
		can_vote = 0;
	}

	// dangling if statement
	if (age > age_threshold){
		can_vote = 1
	}
	if (age){
		can_vote  = 2
	}

}
