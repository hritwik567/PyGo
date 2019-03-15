package main

import "fmt"

func main() int {
  var signal int
  signal = 15

  signal_type := "Signal_type"
  switch signal {
    case 2:
      signal_type = "SIG_INT"
    case 8:
      signal_type = "SIG_FPE"
    case 9:
      signal_type = "SIG_KILL"
    case 11:
      signal_type = "SIG_SEGV"
    case 14:
      signal_type = "SIG_ALRM"
    default:
      signal_type = "Unrecognised Signal"
  }

  switch signal < 31 && signal > 0 {
    case true:
      return 0
    case false:
      return -1
    default:
      return 100
  }
}
