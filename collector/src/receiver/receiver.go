// Package receiver helps to receive broker messages.
package receiver

import (
	"encoding/json"
	"github.com/sirupsen/logrus"
	"github.com/streadway/amqp"
)

// A Message contains broker message structure.
type Message struct {
	Id       string   `json:"id"`
	Title    string   `json:"title"`
	Comments []string `json:"comments"`
	Date     int      `json:"date"`
	Source   string   `json:"source"`
	Body     string   `json:"body"`
	Url      string   `json:"url"`
	Keyword  string   `json:"keyword"`
}

// A Receiver contains broker receiver logic.
type Receiver struct {
	broker *amqp.Channel  // rabbitmq broker channel instance
	logger *logrus.Logger // logger
}

// ReceiveQueue starts receiving broker messages by queue name and parse it to Message, then sends result to the ch.
func (r *Receiver) ReceiveQueue(queue string, ch chan Message) {
	var message Message

	messages, err := r.broker.Consume(
		queue,
		"",
		true,
		false,
		false,
		false,
		nil)

	if err != nil {
		r.logger.Error("error to initiate consumer")

		panic(err)
	}

	forever := make(chan bool)

	go func() {
		for d := range messages {
			err = json.Unmarshal(d.Body, &message)

			if err != nil {
				r.logger.Error("error while unmarshal message")

				panic(err)
			}

			ch <- message
		}
	}()

	r.logger.Infof(" [*] - start waiting for messages on %s queue", queue)
	<-forever
}

// CreateReceiver creates Receiver instance.
func CreateReceiver(ch *amqp.Channel) *Receiver {
	return &Receiver{
		broker: ch,
	}
}
