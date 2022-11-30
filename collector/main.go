package main

import (
	"github.com/codex-team/brand-watcher/collector/pkg/rabbitmq"
	"github.com/codex-team/brand-watcher/collector/src/utils"
)

func main() {
	config := utils.ReadConfigFile("./config.json")

	ch := rabbitmq.ConnectToRabbitMQ(config.RabbitMQUrl)
}
