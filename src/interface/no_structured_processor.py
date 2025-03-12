
from models.exam_classifier import ExamClassifier
import pandas as pd
import torch
from interface.message_sender import MessageSender
from interface.update_sheet import WorksheetUpdater

torch.classes.__path__ = []


class NoStructuredDataProcessor:
    """Processa e envia mensagens para dados não estruturados"""
    
    def __init__(self, df_no_structured: pd.DataFrame, classifier: ExamClassifier, message_sender: MessageSender, worksheet_updater: WorksheetUpdater):
        self.df_no_structured = df_no_structured
        self.classifier = classifier
        self.message_sender = message_sender
        self.worksheet_updater = worksheet_updater

    def process(self):
        """ Envia as mensagens e as registra na planilha da web """
        batch_update_data = []
        # Adiciona as títulos das colunas
        batch_update_data.append({'range': 'G1', 'values': [['STATUS_ENVIO']]}) 
        batch_update_data.append({'range': 'H1', 'values': [['MENSAGEM']]})

        #Envia as mensagens  enquanto registra na tabela o envio.
        for i, row in self.df_no_structured.iterrows():
            phone = row["TEL"]
            name = row["SOLICITANTE"]
            revenue = row["DS_RECEITA"]
            date = row["DATA"]

            if self.classifier.classify_exams(revenue):
                self.message_sender.send(phone, name, revenue, date)
                batch_update_data.append({'range': f'G{i+2}', 'values': [['Enviado']]})
                batch_update_data.append({'range': f'H{i+2}', 'values': [[f'Olá, {name}! Falta você enviar sua imagem relacionada a: {revenue}, exame este realizado em {date}']]})

        self.worksheet_updater.update(batch_update_data)
