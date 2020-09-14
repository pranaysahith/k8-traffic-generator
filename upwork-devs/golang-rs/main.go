package main

import (
	"github.com/tg/generateurl"
	"github.com/tg/log"
)

func main() {

	log.Filelog("urltxt.txt")

	generateurl.Thefile("urltxt.txt", "open")
	generateurl.Thefile("urltxt.txt", "download")
	generateurl.Thefile("urltxt.txt", "upload")

}
