package logger

import (
	log "github.com/sirupsen/logrus"
)

func GetLogger() *log.Logger {
	/* Turn on the color formating
	Use full timestamp */

	var logger = log.New()

	logger.SetFormatter(&log.TextFormatter{
		DisableColors: false,
		FullTimestamp: true,
	})

	return logger
}
