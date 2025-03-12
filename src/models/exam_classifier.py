
from transformers import pipeline
from models.text_cleaner import TextCleaner
from models.img_exam_checker import ImageExamChecker
# classe utilizadas para classificar os textos relacionados a exames de imagem, utilizando lógica de palavra chave e bioBERT(modelo de IA pré-treinado )
class ExamClassifier:
    def __init__(self):
        """
        Classe Facade (Fachada) responsável por inicializa lógica de classificar textos sobre exames.
        """
        self.pipe = pipeline("text-classification", model="dmis-lab/biobert-v1.1") # Modelo de IA pré-treinado

    def classify_exams(self, text) -> bool:
        """
            Método que classifica exames, Espera-se:que retorne True se o texto de exames é relacionado a exames de imagens
        """
        cleaned_text = TextCleaner.clean(text) 
        max_tokens = 120 # Limitar o texto a 512 tokens com margem empirica de segurança
        tokenized_text = cleaned_text.split()[:max_tokens]  # Truncar a lista de palavras
        truncated_text = " ".join(tokenized_text)  # Reconstruir o texto truncado

        # Prompts que auxilia o Modelo de IA a identificar textos relacionados a exames de imagem
        prompt = f"O seguinte texto está ligado a exames médicos que envolvem imagens (como tomografia, ressonância ou radiografia)? texto: {truncated_text}" 

        result = self.pipe(prompt)
        label = result[0]['label']
        score = result[0]['score']

        """ 
            Retorna True se o texto está de acordo com o prompt e pontuou com mais de 70% de chance de confiança na análise 
            OU quando encontra uma palavra chave no texto que indica relação com exames de imagem.
        """
        if (label == 'LABEL_1' and score > 0.7) or ImageExamChecker.contains_image_exam_terms(truncated_text):
            return True
        else:
            return False

