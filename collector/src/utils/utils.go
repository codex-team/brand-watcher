// Package utils contains helpers.
package utils

import (
	"encoding/json"
	"github.com/sirupsen/logrus"
	"io/ioutil"
	"os"
)

// A Config contains config.json structure.
type Config struct {
	RabbitMQUrl string   `json:"rabbitmq-url"`
	Queues      []string `json:"queues"`
}

// ReadConfigFile parse config file in path and returns object with type Config.
func ReadConfigFile(path string, logger *logrus.Logger) Config {
	var config Config

	jsonFile, err := os.Open(path)

	if err != nil {
		logger.Error("error while opening config file")

		panic(err)
	}

	byteValue, _ := ioutil.ReadAll(jsonFile)

	err = json.Unmarshal(byteValue, &config)

	if err != nil {
		logger.Error("error while unmarshal json data")

		panic(err)
	}

	return config
}
