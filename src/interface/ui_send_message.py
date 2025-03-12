from models.exam_classifier import ExamClassifier
from services.publisher import RabbitmqPublisher
from interface.update_sheet import WorksheetUpdater
from interface.message_sender import MessageSender
from interface.structured_processor import StructuredDataProcessor
from interface.no_structured_processor import NoStructuredDataProcessor
from interface.processor import DataProcessor
from typing import Optional
import pandas as pd
import streamlit as st
import gspread
import time

class SendMessageInterface:
    """Classe chamada quando o butão na interface é clicado, esta classe é um Facade (fachada)
        quanda chamada ela aplica a lógica de outras classes para no fim das contas enviar a mensagem através da interface do usuario no Streamlit
    """
    
    def __init__(self, worksheet_structured: Optional[gspread.worksheet.Worksheet], worksheet_no_structured: Optional[gspread.worksheet.Worksheet]):
        # Espera-se que os dados a seguir sejam None ou um objeto gspread manipulável
        self.worksheet_structured = worksheet_structured 
        self.worksheet_no_structured = worksheet_no_structured

        # Espera-se que os dados a seguir sejam None ou um dataFrame
        self.df_structured = self._get_dataframe(self.worksheet_structured)
        self.df_no_structured = self._get_dataframe(self.worksheet_no_structured)

        # Composições
        self.classifier = ExamClassifier() # Para classificar os dados utilizando ML
        self.obj_publisher = RabbitmqPublisher() # Para fazer injeção de dependência ao enviar mensagens

    def _get_dataframe(self, worksheet: Optional[gspread.worksheet.Worksheet]) -> pd.DataFrame:
        """ 
            Retorna o dataFrame de um objeto gspread ,
            útil para mostrar a planilha no streamlit
        """
        if worksheet is not None:
            records = worksheet.get_all_records() # Retona todas as páginas da planilha
            return pd.DataFrame(records) if records else pd.DataFrame()
        return pd.DataFrame()

    def publish_message(self):
        start_time = time.time() # Marcar o tempo para enviar as mensagens desde o clique até a publicaçãodas mensagens na fila.

        message_sender = MessageSender(self.obj_publisher) # Objeto útil para fazer a injeção para publicar as mensagens independente da estrutura dos dados.

        # Atualiza as planilha após os registros das mensagens e suas emissões, Espera-se None ou um objeto gspread
        worksheet_updater_structured = WorksheetUpdater(self.worksheet_structured) 
        worksheet_updater_no_structured = WorksheetUpdater(self.worksheet_no_structured) 


        # Inicializa a lógica para os dados estruturados caso seja um objeto gspread para a manipulação
        if self.worksheet_structured is not None:
            structured_processor = StructuredDataProcessor(self.df_structured, message_sender, DataProcessor(), worksheet_updater_structured)
            structured_processor.process()

        # Inicializa a lógica para os dados não estruturados caso seja o objeto gspread para a manipulação
        if self.worksheet_no_structured is not None:
            no_structured_processor = NoStructuredDataProcessor(self.df_no_structured, self.classifier, message_sender, worksheet_updater_no_structured)
            no_structured_processor.process()
        
        end_time = time.time()
        execution_time = round(end_time - start_time, 2 ) # Arredondando 2 casas decimais

        st.write(f"Mensagens publicadas com sucesso em {execution_time} segundos!") 

