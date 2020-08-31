package generateurl

import (
	"encoding/csv"
	"fmt"
	"io/ioutil"
	"net/http"
	"os"
	"time"

	"github.com/trafficgenerator/config"
)

//Urls is
type Urls struct {
	Name string
	URL  string
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
			cs := Urls{parts[0], parts[1]}
			status = append(status, cs)
		} else {
			break
		}
	}
	fmt.Printf("%+v\n", status)
	client := http.Client{
		Timeout: y * time.Millisecond,
	}

	for _, eachline := range status {

		resp, err := client.Get(eachline.URL)
		if err != nil {
			panic(err)
		}
		/*logfile, err := os.OpenFile("log.log", os.O_RDWR|os.O_CREATE|os.O_APPEND, 0666)
		if err != nil {
			panic(err)
		}
		logger := log.New(logfile, "", log.LstdFlags)
		logger.Println(eachline.URL, "\n", resp.StatusCode, http.StatusText(resp.StatusCode), "\n")
		defer resp.Body.Close()*/
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

	}

}
