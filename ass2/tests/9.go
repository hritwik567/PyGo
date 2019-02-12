package main;

import "fmt";
import "math";

type geometry = interface {
	areas();
};

type rect = struct {
	width, height float64;
};
type circle = struct {
	radius float64;
};


func main() {
	r := rect(3, 4);
	c := circle(5);

	measure(r);
	measure(c);
};
