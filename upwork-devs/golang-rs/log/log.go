package log

import (
	"context"
	"encoding/csv"
	"log"
	"net/http"
	"os"

	"github.com/chromedp/chromedp"
	"github.com/tg/timeresponse"
)

//Urls is
type Urls struct {
	Name string
	URL  string
	Type string
}

//Filelog is
func Filelog(v string) {
	//y := Config()
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
	//	fmt.Printf("%+v\n", status)

	for _, eachline := range status {
		//url := eachline.URL
		//filename := eachline.Name
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
			defer resp.Body.Close()
		} else if eachline.Type == "browser" {
			ctx, cancel := chromedp.NewContext(context.Background(), chromedp.WithDebugf(log.Printf))
			defer cancel()
			time := timeresponse.Getresptime(eachline.URL)
			//var imageBuf []byte
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
