package main

import (
	"encoding/json"

	"github.com/codex-team/brand-watcher/collector/pkg/logger"
	"github.com/codex-team/brand-watcher/collector/pkg/rabbitmq"
	"github.com/codex-team/brand-watcher/collector/src/notification"
	"github.com/codex-team/brand-watcher/collector/src/receiver"
	"github.com/codex-team/brand-watcher/collector/src/utils"
)

func main() {
	log := logger.GetLogger()
	config := utils.ReadConfigFile("./config.json", log)
	ch := rabbitmq.ConnectToRabbitMQ(config.RabbitMQUrl, log)
	rec := receiver.CreateReceiver(ch, log)

	channel := make(chan receiver.Message)

	for _, queue := range config.Queues {
		go rec.ReceiveQueue(queue, channel)
	}

	// Look for data from channel with rabbitmq messages
	for data := range channel {
		log.Info(data)
		out, err := json.Marshal(data)
		if err != nil {
			log.Error(err)
		}
		notification.Notify(config.Webhook, string(out), log)
	}
}
