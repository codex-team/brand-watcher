package receiver

import (
	"encoding/json"
	"fmt"
	"github.com/streadway/amqp"
)

type MessageStruct struct {
	Id       string   `json:"id"`
	Title    string   `json:"title"`
	Comments []string `json:"comments"`
	Date     int      `json:"date"`
	Source   string   `json:"source"`
	Body     string   `json:"body"`
	Url      string   `json:"url"`
	Keyword  string   `json:"keyword"`
}

type Receiver struct {
	broker *amqp.Channel
}

func (r *Receiver) ReceiveQueue(queue string, ch chan MessageStruct) {
	var message MessageStruct

	messages, err := r.broker.Consume(
		queue,
		"",
		true,
		false,
		false,
		false,
		nil)

	if err != nil {
		fmt.Println("Error to initiate consumer")

		panic(err)
	}

	forever := make(chan bool)

	go func() {
		for d := range messages {
			err = json.Unmarshal(d.Body, &message)

			if err != nil {
				fmt.Println("Error while unmarshal message")

				panic(err)
			}

			ch <- message
		}
	}()

	fmt.Printf(" [*] - start waiting for messages on %s queue", queue)
	<-forever
}

func CreateReceiver(ch *amqp.Channel) *Receiver {
	return &Receiver{
		broker: ch,
	}
}
