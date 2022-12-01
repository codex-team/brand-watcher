package main

import (
	"fmt"
	"github.com/codex-team/brand-watcher/collector/pkg/rabbitmq"
	"github.com/codex-team/brand-watcher/collector/src/receiver"
	"github.com/codex-team/brand-watcher/collector/src/utils"
)

func main() {
	config := utils.ReadConfigFile("./config.json")

	ch := rabbitmq.ConnectToRabbitMQ(config.RabbitMQUrl)

	rec := receiver.CreateReceiver(ch)

	channel := make(chan receiver.MessageStruct)

	for _, queue := range config.Queues {
		go rec.ReceiveQueue(queue, channel)
	}

	for data := range channel {
		fmt.Println(data.Title)
	}

}
