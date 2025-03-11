import pywhatkit
import torch

torch.classes.__path__ = []

class WhatsAppMessenger:
    """ Utiliza-se da API da pywhatkit para enviar mensagens no whatsapp """
    def __init__(self):
        """Inicializa a classe sem um número fixo, que será fornecido na chamada."""
        pass

    def send_message(self, phone_number: str, message: str):
        """Envia a mensagem para o número de telefone especificado."""
        try:
            pywhatkit.sendwhatmsg_instantly(phone_number, message, wait_time=20)
            print(f"Mensagem enviada para o Whatsapp: {phone_number}: {message}")
        except Exception as e:
            print(f"Erro ao enviar mensagem para {phone_number}: {e}")

# whatsapp_messenger = WhatsAppMessenger()
# whatsapp_messenger.send_message("+556185614191", "Olá, esta é uma mensagem de teste!")