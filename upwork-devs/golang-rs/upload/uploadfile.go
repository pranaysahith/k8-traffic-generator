package upload

import (
	"fmt"
	"io"
	"net/http"
	"os"
	"text/template"
)

var templates = template.Must(template.ParseFiles("upload.html"))

//Display is
func Display(w http.ResponseWriter, page string, data interface{}) {
	templates.ExecuteTemplate(w, page+".html", data)
}

//UploadFile is
func UploadFile(w http.ResponseWriter, r *http.Request) {
	r.ParseMultipartForm(10 << 20)

	file, handler, err := r.FormFile("myFile")
	if err != nil {
		fmt.Println("Error Retrieving the File")
		fmt.Println(err)
		return
	}

	defer file.Close()
	fmt.Printf("Uploaded File: %+v\n", handler.Filename)
	fmt.Printf("File Size: %+v\n", handler.Size)
	fmt.Printf("MIME Header: %+v\n", handler.Header)

	// Create file
	dst, err := os.Create(handler.Filename)
	defer dst.Close()
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	if _, err := io.Copy(dst, file); err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	fmt.Fprintf(w, "Successfully Uploaded File\n")
}

// UploadHandler is
func UploadHandler(w http.ResponseWriter, r *http.Request) {
	switch r.Method {
	case "GET":
		Display(w, "upload", nil)
	case "POST":
		UploadFile(w, r)
	}
}
