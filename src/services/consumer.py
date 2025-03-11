import pika
from decouple import config
import json  # Para manipular mensagens no formato JSON
import torch

torch.classes.__path__ = []


class RabbitmqConsumer:
    """ Consome os dados da fila de mensageria do RabbitMQ"""
    def __init__(self, callback):
        self.__host = config("RABBITMQ_HOST")
        self.__port = int(config("RABBITMQ_PORT"))
        self.__user = config("RABBITMQ_USER")
        self.__password = config("RABBITMQ_PASSWORD")
        self.__queue = config("RABBITMQ_QUEUE")
        self.__callback = callback
        self.__channel = self.__create_channel()

    def __create_channel(self):
        """ Cria e retorna o canal conectando com a fila a ser consumida"""
        connection_parameters = pika.ConnectionParameters(
            host=self.__host,
            port=self.__port,
            credentials=pika.PlainCredentials(self.__user, self.__password),
        )
        try:
            connection = pika.BlockingConnection(connection_parameters)
            channel = connection.channel()
            channel.queue_declare(queue=self.__queue, durable=True) 

            channel.basic_consume(
                queue=self.__queue,
                auto_ack=True,
                on_message_callback=self.__callback
            )
            print(f"✅ Conexão estabelecida com a fila '{self.__queue}'")
        except Exception as e:
            print(f"❌ Erro ao conectar no RabbitMQ: {e}")
            raise

        return channel

    def start(self):
        """Inicializa o consumidor do RabbitMQ e o mantém ativo"""
        print(f"🎧 Escutando na porta {self.__port} na fila '{self.__queue}'")
        self.__channel.start_consuming()

def callback(ch, method, properties, body):
    """ 
    Chamada sempre que uma mensagem chega na fila para ser consumida,
    sendo responsável por processar a mensagem recebida,
    confirmar o recebimento após a mensagem ser consumida e trata erros
    """
    try:
        message = json.loads(body.decode())  # Esperando mensagem em formato JSON
        phone_number = message.get("phone_number")
        text = message.get("text")

        if not phone_number or not text:
            raise ValueError("Mensagem incompleta: número ou texto ausente.")

        # whatsapp_messenger = WhatsAppMessenger()
        # whatsapp_messenger.send_message(phone_number, text)

        print(f"✅ Mensagem enviada para {phone_number}")
    except Exception as e:
        print(f"❌ Erro ao enviar mensagem para o WhatsApp: {e}")

