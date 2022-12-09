package main

import (
	"fmt"
	"io/ioutil"
	"os"
)

const (
	usbPath = "/Volumes/USB"
	recoveryPath = "/Users/user/Recovered"
)

func main() {
	if _, err := os.Stat(usbPath); os.IsNotExist(err) {
		fmt.Printf("Error: USB drive not found at %s\n", usbPath)
		return
	}
	if _, err := os.Stat(recoveryPath); os.IsNotExist(err) {
		fmt.Printf("Error: recovery directory not found at %s\n", recoveryPath)
		return
	}
	files, err := ioutil.ReadDir(usbPath)
	if err != nil {
		fmt.Printf("Error: failed to read list of files on USB drive: %s\n", err)
		return
	}
	for _, file := range files {
		if !file.IsDir() && file.Name()[0] != '.' {
			continue
		}

		data, err := ioutil.ReadFile(usbPath + "/" + file.Name())
		if err != nil {
			fmt.Printf("Error: failed to read deleted file %s: %s\n", file.Name(), err)
			continue
		}
		err = ioutil.WriteFile(recoveryPath + "/" + file.Name(), data, 0644)
		if err != nil {
			fmt.Printf("Error: failed to write deleted file %s: %s\n", file.Name(), err)
			continue
		}

		fmt.Printf("Recovered deleted file %s\n", file.Name())
	}
}
