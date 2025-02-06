package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"net/http"
	"time"
)

type Response struct {
	PressedKeys []string `json:"pressedkeys"`
}

var sequences = [][]string{
	{"a","b"},
	{"b"},
	{"b"},
  {""},
}

func main() {
	client := &http.Client{}

	for i, seq := range sequences {
		data, _ := json.Marshal(Response{PressedKeys: seq})

		req, err := http.NewRequest("POST", "http://localhost:8080/update", bytes.NewBuffer(data))
		if err != nil {
			fmt.Println("Request error:", err)
			continue
		}
		req.Header.Set("Content-Type", "application/json")

		resp, err := client.Do(req)
		if err != nil {
			fmt.Println("Error sending update:", err)
		} else {
			fmt.Printf("Updated server with sequence %d: %v\n", i+1, seq)
			resp.Body.Close()
		}

		time.Sleep(3 * time.Second)
	}
}
////






























