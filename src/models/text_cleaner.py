import re
import torch

torch.classes.__path__ = []

class TextCleaner:
    """
    Sanitiza partes indesejadas de textos usando REGEX,
    útil para limpar textos que serão interpretados por modelo ML, assim evitando resultados inconsistentes.
    """
    @staticmethod
    def clean(text):
        if not text:  # Verifica se a string é vazia ou None
            return ""  # Retorna uma string vazia se o texto for vazio ou None

        # Se o texto não for uma string, converte para string
        if not isinstance(text, str):
            text = str(text)

        # Remover espaços extras e quebras de linha
        text = re.sub(r'\s+', ' ', text.strip())

        # Remover sequências de símbolos repetidos (ex: "....", "====", "-----")
        text = re.sub(r'(.)\1+', r'\1', text)

        # Remover caracteres irrelevantes (permitir apenas letras, números, espaços, vírgulas, pontos, hífens e sublinhados)
        text = re.sub(r'[^\w\s,.-_]', '', text)

        # Substituir múltiplos sublinhados por um único sublinhado
        text = re.sub(r'_+', '_', text)

        # Substituir múltiplos hífens por um único hífen
        text = re.sub(r'-+', '-', text)

        # Substituir múltiplos sinais de igual por um único sinal de igual
        text = re.sub(r'=+', '=', text)

        return text