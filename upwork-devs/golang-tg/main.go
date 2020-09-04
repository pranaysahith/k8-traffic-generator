package main

import (
	"github.com/trafficgenerator/generateurl"
	"github.com/trafficgenerator/log"
)

func main() {
	log.Filelog("urlText.txt")
	generateurl.Thefile("urlText.txt")

	//hi.Filelog("URLfile.txt")
}
