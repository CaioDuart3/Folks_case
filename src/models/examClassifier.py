import re
from transformers import pipeline
import torch

torch.classes.__path__ = []

class TextCleaner:
    """
    Limpa partes indesejadas de textos usando REGEX
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
class ImageExamChecker:
    # Palavras chaves para auxiliar na identificação de textos que são relacionados a exames de imagem.
    KEYWORDS = [
        "us", "tr", "tc", "tac", "rm", "rx", "digital", "dexa", "pet scan", "rnm",
        "tomografia", "radiografia", "imagem", "imagens", "ultrassom", "ressonância",
        "ecografia", "mamografia", "angiografia", "cintilografia", "fluoroscopia",
        "espectroscopia", "scopia", "densitometria"
    ]
    # Palavras chaves para auxiliar na identificação de textos que NÃO são relacionados a exames de imagem.
    NO_KEYWORDS = [
        "uso oral", "comprimido", "cápsula", "gotas", "xarope", "pomada", "creme",
        "injeção", "vacina", "dose", "tratamento", "uso tópico", "via sublingual",
        "via intramuscular", "via intravenosa", "via retal", "via nasal", "via ocular",
        "hemograma", "sorologia", "urocultura", "PCR", "VHS", "creatinina", "glicemia",
        "colesterol", "triglicerídeos", "hormônio", "tipagem sanguínea", "antígeno",
        "imunoglobulina", "prova de função hepática", "eletrólitos", "cultura bacteriana"
    ]

    # Método utilizado para identicar a existência de palavras chaves nos textos
    @classmethod
    def contains_image_exam_terms(cls, text):
        text_lower = text.lower()
        # Verifica se há palavras que garantem que NÃO é um exame de imagem
        if any(term in text_lower for term in cls.NO_KEYWORDS):
            return False
        # Verifica se há palavras que indicam exame de imagem
        return any(term in text_lower for term in cls.KEYWORDS)

# classe utilizadas para classificar os textos relacionados a exames de imagem, utilizando lógica de palavra chave e bioBERT(modelo de IA pré-treinado )
class ExamClassifier:
    def __init__(self):
        """
        Classifica textos utilizando modelo de IA pré-treinada e identificação de palavras chaves
        retorna True se a IA identificou um sentimentou positivo em relação ao prompt com mais de 70% de confiabilidade ou identificou uma palavra chave.
        
        """
        self.pipe = pipeline("text-classification", model="dmis-lab/biobert-v1.1") # Modelo de IA pré-treinado utilizado

    def classify_exams(self, text):
        cleaned_text = TextCleaner.clean(text) 
        max_tokens = 120 # Limitar o texto a 512 tokens com margem empirica de segurança
        tokenized_text = cleaned_text.split()[:max_tokens]  # Truncar a lista de palavras
        truncated_text = " ".join(tokenized_text)  # Reconstruir o texto truncado

        # Prompts que auxilia o Modelo de IA a identificar textos relacionados a exames de imagem
        prompt = f"O seguinte texto está ligado a exames médicos que envolvem imagens (como tomografia, ressonância ou radiografia)? texto: {truncated_text}" 

        result = self.pipe(prompt)
        label = result[0]['label']
        score = result[0]['score']

        if (label == 'LABEL_1' and score > 0.7) or ImageExamChecker.contains_image_exam_terms(truncated_text):
            return True
        else:
            return False

