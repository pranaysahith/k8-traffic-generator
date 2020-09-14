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
func Thefile(m string, thetype string) {
	y, _ := config.Config()

	status := []Urls{}
	file, _ := os.Open(m)
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
		//if thetype =="download"{
		if eachline.Type == "request" || thetype == "download" {
			resp, err := client.Get(eachline.URL)
			if err != nil {
				panic(err)
			}

			//	time := timeresponse.Getresptime(eachline.URL)

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

		} else if eachline.Type == "browser" || thetype == "open" {
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
		} else if thetype == "upload" {
			client := &http.Client{}
			f, err := os.Open("aa.txt")
			if err != nil {
				panic(err)
			}
			defer f.Close()
			//	postData := make([]byte, 100)
			req, err := http.NewRequest("POST", eachline.URL, f)
			//req, err := http.NewRequest("POST", eachline.URL, bytes.NewReader(postData))
			if err != nil {
				os.Exit(1)
			}
			req.Header.Add("User-Agent", "myClient")
			resp, err := client.Do(req)
			if err != nil {
				panic(err)
			}
			defer resp.Body.Close()
			fmt.Println(resp, "/n")

		} else {
			break
		}
	}

}
