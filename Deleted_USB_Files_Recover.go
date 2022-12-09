package main

import (
	"fmt"
	"io/ioutil"
	"os"
)

const (
	// The path to the USB drive that we want to recover deleted files from
	usbPath = "/Volumes/USB"

	// The path to the directory where we want to store the recovered files
	recoveryPath = "/Users/user/Recovered"
)

func main() {
	// Check if the USB drive exists
	if _, err := os.Stat(usbPath); os.IsNotExist(err) {
		fmt.Printf("Error: USB drive not found at %s\n", usbPath)
		return
	}

	// Check if the recovery directory exists
	if _, err := os.Stat(recoveryPath); os.IsNotExist(err) {
		fmt.Printf("Error: recovery directory not found at %s\n", recoveryPath)
		return
	}

	// Read the list of files on the USB drive
	files, err := ioutil.ReadDir(usbPath)
	if err != nil {
		fmt.Printf("Error: failed to read list of files on USB drive: %s\n", err)
		return
	}

	// Check each file on the USB drive
	for _, file := range files {
		// Skip files that have not been deleted
		if !file.IsDir() && file.Name()[0] != '.' {
			continue
		}

		// Read the contents of the deleted file
		data, err := ioutil.ReadFile(usbPath + "/" + file.Name())
		if err != nil {
			fmt.Printf("Error: failed to read deleted file %s: %s\n", file.Name(), err)
			continue
		}

		// Write the contents of the deleted file to the recovery directory
		err = ioutil.WriteFile(recoveryPath + "/" + file.Name(), data, 0644)
		if err != nil {
			fmt.Printf("Error: failed to write deleted file %s: %s\n", file.Name(), err)
			continue
		}

		fmt.Printf("Recovered deleted file %s\n", file.Name())
	}
}
