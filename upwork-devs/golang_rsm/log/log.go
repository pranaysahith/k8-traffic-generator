package log

import (
	"context"
	"encoding/csv"
	"log"
	"net/http"
	"os"
	"time"

	"github.com/chromedp/chromedp"
	"github.com/tgg/timeresponse"
)

//Urls is
type Urls struct {
	Name string
	URL  string
	Type string
}

//Profile is
type Profile struct {
	Name    time.Duration
	Status  int
	Hobbies []string
}

//Filelog is
func Filelog(v string) {
	status := []Urls{}

	file, _ := os.Open(v)
	defer file.Close()
	r := csv.NewReader(file)
	for {
		if parts, err := r.Read(); err == nil {
			cs := Urls{parts[0], parts[1], parts[2]}
			status = append(status, cs)
		} else {
			break
		}
	}

	for _, eachline := range status {
		if eachline.Type == "request" {
			resp, err := http.Get(eachline.URL)
			if err != nil {
				panic(err)
			}

			time := timeresponse.Getresptime(eachline.URL)

			logfile, err := os.OpenFile("logrequest.log", os.O_RDWR|os.O_CREATE|os.O_APPEND, 0666)
			if err != nil {
				panic(err)
			}
			
			logger := log.New(logfile, "", log.LstdFlags)
			logger.Println(eachline.URL, resp.StatusCode, http.StatusText(resp.StatusCode), time)
			log.Println(time)
			defer resp.Body.Close()
		} else if eachline.Type == "browser" {
			ctx, cancel := chromedp.NewContext(context.Background(), chromedp.WithDebugf(log.Printf))
			defer cancel()
			time := timeresponse.Getresptime(eachline.URL)
			if err := chromedp.Run(ctx); err != nil {
				log.Fatal(err)
			}

			logfile, err := os.OpenFile("logbrowser.log", os.O_RDWR|os.O_CREATE|os.O_APPEND, 0666)
			if err != nil {
				panic(err)
			}

			logger := log.New(logfile, "", log.LstdFlags)
			logger.Println(eachline.URL, time)

		} else {
			break
		}
	}
}
