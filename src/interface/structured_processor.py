from interface.message_sender import MessageSender
from interface.processor import DataProcessor
from interface.update_sheet import WorksheetUpdater
import pandas as pd

class StructuredDataProcessor:
    """Processa e envia mensagens para dados estruturados"""
    
    def __init__(self, df_structured: pd.DataFrame, message_sender: MessageSender, data_processor: DataProcessor, worksheet_updater: WorksheetUpdater):
        self.df_structured = df_structured
        self.message_sender = message_sender
        self.data_processor = data_processor
        self.worksheet_updater = worksheet_updater

    def process(self):
        """ Envia as mensagens e as registra na planilha da web"""
        batch_update_data = []
        data_filtered = self.data_processor.filter_data_for_tuss(self.df_structured)

        # Adiciona as títulos das colunas
        batch_update_data.append({'range': 'H1', 'values': [['STATUS_ENVIO']]})
        batch_update_data.append({'range': 'I1', 'values': [['MENSAGEM']]})
        
        #Envia as mensagens  enquanto registra na tabela o envio.
        for i, row in data_filtered.iterrows():
            phone = row["TEL"]
            name = row["SOLICITANTE"]
            revenue = row["DS_RECEITA"]
            date = row["DATA"]

            self.message_sender.send(phone, name, revenue, date)
            batch_update_data.append({'range': f'H{i+2}', 'values': [['Enviado']]})
            batch_update_data.append({'range': f'I{i+2}', 'values': [[f'Olá, {name}! Falta você enviar sua imagem relacionada a: {revenue}, exame este realizado em {date}']]})

        self.worksheet_updater.update(batch_update_data)
