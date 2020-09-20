package timeresponse

import (
	"fmt"
	"log"
	"net/http"
	"time"
)

// Getresptime is
func Getresptime(url string) time.Duration {
	timestart := time.Now()
	resp, err := http.Get(url)
	if err != nil {
		log.Printf("Error fetching: %v", err)
	}
	defer resp.Body.Close()
	fmt.Println(time.Since(timestart), url)
	return time.Since(timestart)
}
