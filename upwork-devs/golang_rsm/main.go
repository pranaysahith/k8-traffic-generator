package main

import (
	"encoding/json"
	"net/http"
	"time"

	"github.com/rs/cors"
	"github.com/tgg/datajson"
)

type Duration struct {
	time.Duration
}

func (d Duration) MarshalJSON() ([]byte, error) {
	return json.Marshal(d.String())
}

type Message struct {
	Elapsed Duration `json:"elapsed"`
}

func main() {
	mux := http.NewServeMux()
	mux.HandleFunc("/api", datajson.Foo)

	//cors.Default() setup the middleware with default options being
	// all origins accepted with simple methods (GET, POST). See
	// documentation below for more options.
	handler := cors.Default().Handler(mux)
	http.ListenAndServe(":10000", handler)

}
