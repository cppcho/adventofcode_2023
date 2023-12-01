package main

import (
	"fmt"
	"os"

	"github.com/cppcho/adventofcode_2023/day1"
)

func main() {
	fmt.Println("adventofcode_2023")
	args := os.Args

	days := map[string]func(){
		"day1": day1.Run,
	}

	if len(args) > 1 {
		fn, found := days[args[1]]
		if !found {
			panic(fmt.Sprintf("Error: invalid argument: %s", args[1]))
		}
		fn()
	} else {
		fmt.Printf("Error: should specify one or more arguments")
	}

	fmt.Println("end")
}
