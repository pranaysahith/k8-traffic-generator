package main

import (
	"net/http"

	"github.com/tg/generateurl"
	"github.com/tg/log"
	"github.com/tg/upload"
)

func main() {
	go func() {
		log.Filelog("urltxt.txt")
		generateurl.Thefile("urltxt.txt")
	}()
	// Upload route
	http.HandleFunc("/upload", upload.UploadHandler)

	//Listen on port 8080
	http.ListenAndServe(":8080", nil)
}
