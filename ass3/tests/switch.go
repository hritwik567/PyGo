package main

func main() {
	var c = "w"
	switch c {
	case "w":
		fallthrough
	case "W":
		wflg = 1
	case "t":
		fallthrough
	case "T":
		tflg = 1
	case "d":
		dflg = 1
	}
}
