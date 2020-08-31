package log

import (
	"encoding/csv"
	"log"
	"net/http"
	"os"
)

//Urls is
type Urls struct {
	Name string
	URL  string
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
			cs := Urls{parts[0], parts[1]}
			status = append(status, cs)
		} else {
			break
		}
	}

	for _, eachline := range status {

		resp, err := http.Get(eachline.URL)
		if err != nil {
			panic(err)
		}
		logfile, err := os.OpenFile("log.log", os.O_RDWR|os.O_CREATE|os.O_APPEND, 0666)
		if err != nil {
			panic(err)
		}
		logger := log.New(logfile, "", log.LstdFlags)
		logger.Println(eachline.URL, "\n", resp.StatusCode, http.StatusText(resp.StatusCode), "\n")
		defer resp.Body.Close()
	}
}
