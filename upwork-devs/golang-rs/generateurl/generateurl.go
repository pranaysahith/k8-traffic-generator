package generateurl

import (
	"context"
	"encoding/csv"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"os"
	"time"

	"github.com/chromedp/chromedp"
	"github.com/tg/config"
	"github.com/tg/screenshot"
)

//Urls is
type Urls struct {
	Name string
	URL  string
	Type string
}

//Thefile is
func Thefile(x string) {
	y := config.Config()

	status := []Urls{}
	file, _ := os.Open(x)
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
	fmt.Printf("%+v", status)
	client := http.Client{
		Timeout: y * time.Millisecond,
	}

	for _, eachline := range status {
		url := eachline.URL
		filename := eachline.Name

		if eachline.Type == "request" {
			resp, err := client.Get(eachline.URL)
			if err != nil {
				panic(err)
			}

			/*time := timeresponse.Getresptime(eachline.URL)

			/*logfile, err := os.OpenFile("logrequst.log", os.O_RDWR|os.O_CREATE|os.O_APPEND, 0666)
			if err != nil {
				panic(err)
			}
			logger := log.New(logfile, "", log.LstdFlags)
			logger.Println(eachline.URL, resp.StatusCode, http.StatusText(resp.StatusCode), time)
			defer resp.Body.Close()
			*/
			html, err := ioutil.ReadAll(resp.Body)
			if err != nil {
				panic(err)
			}
			f, err := os.Create(eachline.Name)
			if err != nil {
				panic(err)
			}
			defer f.Close()
			err = ioutil.WriteFile(eachline.Name, html, 0644)
			if err != nil {
				panic(err)
			}

		} else if eachline.Type == "browser" {
			ctx, cancel := chromedp.NewContext(context.Background(), chromedp.WithDebugf(log.Printf))
			defer cancel()
			//time := timeresponse.Getresptime(eachline.URL)
			var imageBuf []byte
			if err := chromedp.Run(ctx, screenshot.ScreenshotTasks(url, &imageBuf)); err != nil {
				log.Fatal(err)
			}
			/*if err := chromedp.Run(ctx); err != nil {
				log.Fatal(err)
			}*/
			if err := ioutil.WriteFile(filename, imageBuf, 0644); err != nil {
				log.Fatal(err)
			}
			/*logfile, err := os.OpenFile("logbrowser.log", os.O_RDWR|os.O_CREATE|os.O_APPEND, 0666)
			if err != nil {
				panic(err)
			}
			logger := log.New(logfile, "", log.LstdFlags)
			logger.Println(eachline.URL, time)*/

		} else {
			break
		}
	}

}
