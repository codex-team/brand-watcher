// Package rabbitmq consists logic of connection to rabbitmq.
package rabbitmq

import (
	"fmt"
	"github.com/streadway/amqp"
)

// ConnectToRabbitMQ create a connection with rabbitmq by url and returns rabbitmq channel.
func ConnectToRabbitMQ(rabbitmqUrl string) *amqp.Channel {
	conn, err := amqp.Dial(rabbitmqUrl)

	if err != nil {
		fmt.Println("Error while connecting to RabbitMQ")
		panic(err)
	}

	fmt.Println("Connected to RabbitMQ")

	ch, err := conn.Channel()

	if err != nil {
		fmt.Println("Error while creating rabbitmq channel")
		panic(err)
	}

	return ch
}
