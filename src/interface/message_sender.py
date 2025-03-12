
from services.publisher import RabbitmqPublisher

class MessageSender:
    """Envia mensagens via RabbitMQ"""
    
    def __init__(self, publisher: RabbitmqPublisher): # injeção de dependência
        self.publisher = publisher # objeto

    def send(self, phone: str, name: str, revenue: str, date: str):
        """publica a mensagem no rabbitMQ"""
        self.publisher.send_message({
            "phone_number": "+55" + str(phone),
            "text": f"Olá, {name}! Falta você enviar sua imagem relacionada a: {revenue}, exame este realizado em {date}."
        })
