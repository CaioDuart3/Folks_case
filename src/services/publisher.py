from decouple import config
from typing import Dict
import json
import pika
import torch

torch.classes.__path__ = []

class RabbitmqPublisher:
    """ Classe utilizada para publicar mensagens no serviço de mensageria RabbitMQ"""

    def __init__(self):
        self.__host = config("RABBITMQ_HOST")
        self.__port = int(config("RABBITMQ_PORT"))
        self.__user = config("RABBITMQ_USER")
        self.__password = config("RABBITMQ_PASSWORD")
        self.__exchange = config("RABBITMQ_EXCHANGE")
        self.__routing_key = config("RABBITMQ_ROUTING_KEY")
        self.__queue = config("RABBITMQ_QUEUE")  # Adicionado para garantir a existência da fila
        self.__channel, self.__connection = self.__create_channel()

    def __create_channel(self):
        """Cria um canal conectado a fila de mensagens"""
        connection_parameters = pika.ConnectionParameters(
            host=self.__host,
            port=self.__port,
            credentials=pika.PlainCredentials(self.__user, self.__password),
        )
        try:
            connection = pika.BlockingConnection(connection_parameters)
            channel = connection.channel()

            # Garante que a fila exista
            channel.queue_declare(queue=self.__queue, durable=True)

            print(f"✅ Conexão estabelecida com RabbitMQ no host {self.__host}:{self.__port}")
        except Exception as e:
            print(f"❌ Erro ao conectar no RabbitMQ: {e}")
            raise
        return channel, connection

    def send_message(self, body: Dict):
        """
        Publica mensagens enviando para a Exchange, recebendo em seu argumento contendo,
        contendo o número e a mensagem para a pessoa.

        Exemplo de argumentos:
        {"phone": "+5516912345678", "message":"Olá, mundo!" }
        """
        try:
            if "phone_number" not in body or "text" not in body:
                raise ValueError("Mensagem inválida: 'phone_number' e 'text' são obrigatórios.")

            self.__channel.basic_publish(
                exchange=self.__exchange, 
                routing_key=self.__routing_key,
                body=json.dumps(body),
                properties=pika.BasicProperties(
                    delivery_mode=2  # Torna a mensagem persistente
                )
            )
            print(f"📩 Mensagem publicada com sucesso: {body}")
        except Exception as e:
            print(f"❌ Erro ao publicar a mensagem: {e}")
            raise


