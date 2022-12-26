// Package notification sends messages to telegram using webhook bot.
package notification

import (
	"net/http"
	"net/url"
	"strings"

	"github.com/sirupsen/logrus"
)

type Message struct {
	Message string `json:"message"`
}

func Notify(webhook string, msg string, log *logrus.Logger) {
	payload := url.Values{}
	payload.Set("message", msg)

	_, err := http.Post(webhook, "application/x-www-form-urlencoded", strings.NewReader(payload.Encode()))

	if err != nil {
		log.Error("Could not make POST request to " + webhook)
	}
}
