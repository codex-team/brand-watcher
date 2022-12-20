// Package logger handle logging process to stdout with detailed timestamp
package logger

import (
	log "github.com/sirupsen/logrus"
)

// GetLogger return logger with formatted colors and timestamp
func GetLogger() *log.Logger {
	var logger = log.New()

	logger.SetFormatter(&log.TextFormatter{
		DisableColors: false,
		FullTimestamp: true,
		ForceColors:   true,
	})

	return logger
}
