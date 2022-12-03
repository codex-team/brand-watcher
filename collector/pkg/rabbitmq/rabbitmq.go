// Package rabbitmq consists logic of connection to rabbitmq.
package rabbitmq

import (
	"github.com/sirupsen/logrus"
	"github.com/streadway/amqp"
)

// ConnectToRabbitMQ create a connection with rabbitmq by url and returns rabbitmq channel.
func ConnectToRabbitMQ(rabbitmqUrl string, logger *logrus.Logger) *amqp.Channel {
	conn, err := amqp.Dial(rabbitmqUrl)

	if err != nil {
		logger.Error("error while connecting to RabbitMQ")
		panic(err)
	}

	logger.Info("connected to RabbitMQ")

	ch, err := conn.Channel()

	if err != nil {
		logger.Error("error while creating rabbitmq channel")
		panic(err)
	}

	return ch
}
