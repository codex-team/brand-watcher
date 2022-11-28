package utils

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"os"
)

type Config struct {
	RabbitMQUrl string   `json:"rabbitmq-url"`
	Queues      []string `json:"queues"`
}

func ReadConfigFile(path string) Config {
	var config Config

	jsonFile, err := os.Open(path)

	if err != nil {
		fmt.Println("Error while opening config file")

		panic(err)
	}

	byteValue, _ := ioutil.ReadAll(jsonFile)

	err = json.Unmarshal(byteValue, &config)

	if err != nil {
		fmt.Println("Error while unmarshal json data")

		panic(err)
	}

	return config
}
