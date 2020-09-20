package datajson

import (
	"encoding/csv"
	"encoding/json"
	"net/http"
	"os"
	"time"

	"github.com/tgg/timeresponse"
	"github.com/tgg/generateurl"
	"github.com/tgg/log"
	
)

//Urls is
type Urls struct {
	Name string
	URL  string
	Type string
}

//Profile is
type Profile struct {
	Timeresp Duration `json:"timeresp"`
	Status   int      `json:"status"`
	Urll     string   `json:"urll"`
}
type Profiles []Profile

type Profilet struct {
	Timeresp []byte
	Status   int
	Urll     string
}
type Profilest []Profilet

type Duration struct {
	time.Duration
}

func (d Duration) MarshalJSON() ([]byte, error) {
	return json.Marshal(d.String())
}

type Message struct {
	Time   Duration `json:"time"`
	Status int
	Urll   string
}
type Messages []Message

//Foo is
func Foo(w http.ResponseWriter, r *http.Request) {
	status := []Urls{}

	file, _ := os.Open("urltxt.txt")
	defer file.Close()
	m := csv.NewReader(file)
	for {
		if parts, err := m.Read(); err == nil {
			cs := Urls{parts[0], parts[1], parts[2]}
			status = append(status, cs)
		} else {
			break
		}
	}

	var s []Profile
	for _, eachline := range status {
		resp, err := http.Get(eachline.URL)
		if err != nil {
			panic(err)
		}
		
		profiless := []Profile{
			{Duration{timeresponse.Getresptime(eachline.URL)}, resp.StatusCode, eachline.URL},
		}

		s = append(s, profiless...)
			generateurl.Thefile("urltxt.txt", "upload")
			generateurl.Thefile("urltxt.txt", "download")
			log.Filelog("urltxt.txt")
			generateurl.Thefile("urltxt.txt", "open")
	}
	
	json.NewEncoder(w).Encode(s)
}
