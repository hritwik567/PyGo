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

func (|r rect|) area() float64 {
	return r.width * r.height;
};

type rect = struct {
	width, height float64;
};
type circle = struct {
	radius float64;
};

func (|r rect|) area() float64 {
	return r.width * r.height;
};



func main() {
	r := rect(3, 4);
	c := circle(5);

	measure(r);
	measure(c);
};
