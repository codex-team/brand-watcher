package main

import (
	"fmt"

	"github.com/codex-team/brand-watcher/collector/pkg/logger"
	"github.com/codex-team/brand-watcher/collector/pkg/rabbitmq"
	"github.com/codex-team/brand-watcher/collector/src/utils"
)

func main() {
	config := utils.ReadConfigFile("./config.json")

	rabbitmq.ConnectToRabbitMQ(config.RabbitMQUrl)
	log := logger.GetLogger()
	log.Info(fmt.Sprintf("Connected to rabbitmq with url: %s", config.RabbitMQUrl))
}
