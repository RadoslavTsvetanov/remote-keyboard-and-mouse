package main

import (
	"encoding/json"
	"fmt"
	"net/http"
	"sync"
	"time"

	"github.com/rs/cors"
)

type Response struct {
	PressedKeys []string `json:"pressedkeys"`
}

type Dimension struct{
	X int `json:"x"`
	Y int `json:"y"`
}

type MouseData struct {
	X      int    `json:"x"`
	Y      int    `json:"y"`
	Action string `json:"action"` // Action could be "move", "click", or "move+click"
	Dimensions Dimension `json:"dimensions"` 
}

var (
	keySequence = Response{PressedKeys: []string{"ctrl", "alt", "del"}}
	mouse       = MouseData{X: 0, Y: 0, Action: "move"} // Initialize mouse data with default values
	mu          sync.Mutex
)

func getKeysHandler(w http.ResponseWriter, r *http.Request) {
	mu.Lock()
	defer mu.Unlock()

	// Refresh the mouse data to none/null

	w.Header().Set("Content-Type", "application/json")
	// Encode both keySequence and mouse data in the response
	response := struct {
		Keys  Response  `json:"keys"`
		Mouse MouseData `json:"mouse"`
	}{
		Keys:  keySequence,
		Mouse: mouse,
	}
	json.NewEncoder(w).Encode(response)


	mouse = MouseData{X: 0, Y: 0, Action: ""}
}

func updateKeysHandler(w http.ResponseWriter, r *http.Request) {
	mu.Lock()
	defer mu.Unlock()

	var newKeys Response
	if err := json.NewDecoder(r.Body).Decode(&newKeys); err != nil {
		http.Error(w, "Invalid request body", http.StatusBadRequest)
		return
	}

	keySequence = newKeys
	fmt.Println("Updated key sequence:", newKeys.PressedKeys)
	w.WriteHeader(http.StatusOK)
}

func updateMouseDataHandler(w http.ResponseWriter, r *http.Request) {
	mu.Lock()
	defer mu.Unlock()

	var newMouse MouseData
	if err := json.NewDecoder(r.Body).Decode(&newMouse); err != nil {
		http.Error(w, "Invalid request body", http.StatusBadRequest)
		return
	}

	// Update the mouse data
	mouse = newMouse
	fmt.Println("Updated mouse data:", newMouse)
	w.WriteHeader(http.StatusOK)
}

func main() {
	// Set up the CORS middleware
	corsHandler := cors.New(cors.Options{
		AllowedOrigins: []string{"*"}, // Allow all origins, you can restrict it to specific domains
		AllowedMethods: []string{"GET", "POST", "PUT", "DELETE", "OPTIONS"},
		AllowedHeaders: []string{"Content-Type", "Authorization"},
	})

	// Create the mux and handlers
	mux := http.NewServeMux()
	mux.HandleFunc("/keys", getKeysHandler)
	mux.HandleFunc("/update", updateKeysHandler)
	mux.HandleFunc("/updateMouse", updateMouseDataHandler) // New POST endpoint for updating mouse data

	// Wrap the mux with the CORS handler
	handler := corsHandler.Handler(mux)

	// Set up and start the HTTP server
	server := &http.Server{
		Addr:         ":8080",
		Handler:      handler,
		ReadTimeout:  5 * time.Second,
		WriteTimeout: 5 * time.Second,
	}

	fmt.Println("Server started on :8080")
	if err := server.ListenAndServe(); err != nil {
		fmt.Println("Server error:", err)
	}
}
