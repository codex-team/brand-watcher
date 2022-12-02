package main

import (
	"fmt"

	"github.com/codex-team/brand-watcher/collector/pkg/logger"
	"github.com/codex-team/brand-watcher/collector/pkg/rabbitmq"
	"github.com/codex-team/brand-watcher/collector/src/receiver"
	"github.com/codex-team/brand-watcher/collector/src/utils"
)

func main() {
	log := logger.GetLogger()
	config := utils.ReadConfigFile("./config.json")
	ch := rabbitmq.ConnectToRabbitMQ(config.RabbitMQUrl)
	log.Info(fmt.Sprintf("Connected to rabbitmq with url: %s", config.RabbitMQUrl))
	rec := receiver.CreateReceiver(ch)

	channel := make(chan receiver.Message)

	for _, queue := range config.Queues {
		go rec.ReceiveQueue(queue, channel)
	}

	for data := range channel {
		fmt.Println(data.Title)
	}
}
