package main

import (
	"github.com/codex-team/brand-watcher/server/pkg/logger"
	"github.com/codex-team/brand-watcher/server/pkg/notification"
	"github.com/codex-team/brand-watcher/server/src/utils"
)

func main() {
	log := logger.GetLogger()

	log.Info("Start sending notifications")
	config := utils.ReadConfigFile("./config.json", log)
	notification.Notify(config.Webhook, config.Message, log)
}
