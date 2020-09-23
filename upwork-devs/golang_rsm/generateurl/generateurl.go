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
	"github.com/tgg/config"
	"github.com/tgg/screenshot"
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
		if eachline.Type == "request" || thetype == "download" {
			resp, err := client.Get(eachline.URL)
			if err != nil {
				panic(err)
			}

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
			var imageBuf []byte
			if err := chromedp.Run(ctx, screenshot.ScreenshotTasks(url, &imageBuf)); err != nil {
				log.Fatal(err)
			}

			if err := ioutil.WriteFile(filename, imageBuf, 0644); err != nil {
				log.Fatal(err)
			}
			
		} else if thetype == "upload" {
			client := &http.Client{}
			f, err := os.Open("aa.txt")
			if err != nil {
				panic(err)
			}

			defer f.Close()
			req, err := http.NewRequest("POST", eachline.URL, f)
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
