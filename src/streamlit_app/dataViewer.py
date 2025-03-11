
from models.examClassifier import ExamClassifier
from services.consumer import RabbitmqConsumer
from services.publisher import RabbitmqPublisher
from services.consumer import callback
from decouple import config
import pandas as pd
import streamlit as st
import gspread
import torch
from typing import Optional

torch.classes.__path__ = []

def filter_data_for_tuss(dataframe : pd.DataFrame) -> pd.DataFrame:
    sheet_url = config("REFERENCE_SPREADSHEET")
    tuss_worksheet = pd.read_csv(sheet_url)
    tuss_codes = tuss_worksheet['TUSS'].astype(str).tolist()
    filtered_data = dataframe[dataframe['CD_TUSS'].apply(lambda x: str(x) in tuss_codes)]
    return filtered_data

class MessagePublisher:
    
    def __init__(self, worksheet_structured: Optional[gspread.worksheet.Worksheet], worksheet_no_structured: Optional[gspread.worksheet.Worksheet]):
        self.worksheet_structured = worksheet_structured
        self.worksheet_no_structured = worksheet_no_structured
        self.df_structured = self._get_dataframe(self.worksheet_structured)
        self.df_no_structured = self._get_dataframe(self.worksheet_no_structured)
        self.classifier = ExamClassifier()
        self.obj_publisher = RabbitmqPublisher()

    def _get_dataframe(self, worksheet: Optional[gspread.worksheet.Worksheet]) -> pd.DataFrame:
        if worksheet is not None:
            records = worksheet.get_all_records()
            return pd.DataFrame(records) if records else pd.DataFrame()
        return pd.DataFrame()

    def _send_message(self, phone: str, name: str, revenue: str, date: str):
        self.obj_publisher.send_message({
            "phone_number": "+55" + str(phone),
            "text": f"Olá, {name}! Falta você enviar sua imagem relacionada a: {revenue}, exame este realizado em {date}."
        })

    def _update_worksheet(self, worksheet: Optional[gspread.worksheet.Worksheet], batch_update_data: list):
        if worksheet is not None and batch_update_data:
            worksheet.batch_update(batch_update_data)

    def _process_structured_data(self, df_structured: pd.DataFrame, batch_update_data: list):
        dataFrame_filtered = filter_data_for_tuss(df_structured)
        batch_update_data.append({'range': 'H1', 'values': [['STATUS_ENVIO']]})
        
        for i, row in dataFrame_filtered.iterrows():
            phone = row["TEL"]
            name = row["SOLICITANTE"]
            revenue = row["DS_RECEITA"]
            date = row["DATA"]

            self._send_message(phone, name, revenue, date)
            batch_update_data.append({'range': f'H{i+2}', 'values': [['Enviado']]})
            batch_update_data.append({'range': f'I{i+2}', 'values': [['f"Olá, {name}! Falta você enviar sua imagem relacionada a: {revenue}, exame este realizado em {date}."o']]})

    def _process_no_structured_data(self, df_no_structured: pd.DataFrame, batch_update_data: list):
        batch_update_data.append({'range': 'G1', 'values': [['STATUS_ENVIO']]})

        for i, row in df_no_structured.iterrows():
            phone = row["TEL"]
            name = row["SOLICITANTE"]
            revenue = row["DS_RECEITA"]
            date = row["DATA"]

            if self.classifier.classify_exams(revenue):
                self._send_message(phone, name, revenue, date)
                batch_update_data.append({'range': f'G{i+2}', 'values': [['Enviado']]})
                batch_update_data.append({'range': f'H{i+2}', 'values': [[f'Olá, {name}! Falta você enviar sua imagem relacionada a: {revenue}, exame este realizado em {date}']]})

    def publish_message(self):
        batch_update_data = []

        if self.worksheet_structured is not None:
            self._process_structured_data(self.df_structured, batch_update_data)

        if self.worksheet_no_structured is not None:
            self._process_no_structured_data(self.df_no_structured, batch_update_data)

        self._update_worksheet(self.worksheet_structured, batch_update_data)
        self._update_worksheet(self.worksheet_no_structured, batch_update_data)
        
        obj_consumer = RabbitmqConsumer(callback)
        st.write("Mensagens publicadas com sucesso!")
        obj_consumer.start()


class DataViewer:
    def __init__(self, worksheet_structured: Optional[gspread.worksheet.Worksheet], worksheet_no_structured: Optional[gspread.worksheet.Worksheet]):
        self.worksheet_structured = worksheet_structured
        self.worksheet_no_structured = worksheet_no_structured
        self.df_structured = self._get_dataframe(self.worksheet_structured)
        self.df_no_structured = self._get_dataframe(self.worksheet_no_structured)
        self.USER = config("USERNAME_STREAMLIT")
        self.PASSWORD = config("PASSWORD_STREAMLIT")
        
    def _get_dataframe(self, worksheet: Optional[gspread.worksheet.Worksheet]) -> pd.DataFrame:
        if worksheet is not None:
            records = worksheet.get_all_records()
            return pd.DataFrame(records) if records else pd.DataFrame()
        return pd.DataFrame()

    def authenticate(self) -> bool:
        username = st.text_input("Usuário")
        password = st.text_input("Senha", type="password")
        return username == self.USER and password == self.PASSWORD

    def display_data(self):
        if self.authenticate():
            st.success("Bem-vindo! Aqui estão os dados.")
            option = st.selectbox("Selecione a opção desejada", ["Visualização de Dados Estruturados", "Visualização de Dados Não Estruturados", "Visualizar todos os dados"])
            st.markdown(f"[Clique aqui para acessar o Looker studio!]({config('DATA_VIEW_LINK')})")
            if option == "Visualização de Dados Estruturados":
                self.show_structured_data()
            elif option == "Visualização de Dados Não Estruturados":
                self.show_no_structured_data()
            elif option == "Visualizar todos os dados":
                self.show_all_data()

    def show_structured_data(self):
        
        st.title("Visualização de Dados Estruturados")
        st.dataframe(self.df_structured)
        st.write("### Informações Gerais")
        st.write(self.df_structured.describe())
        if st.button("Enviar mensagem"):
            MessagePublisher(self.worksheet_structured, None).publish_message()

    def show_no_structured_data(self):
        
        st.title("Visualização de Dados Não Estruturados")
        st.dataframe(self.df_no_structured)
        st.write("### Informações Gerais")
        st.write(self.df_no_structured.describe())
        if st.button("Enviar mensagem"):
            MessagePublisher(None, self.worksheet_no_structured).publish_message()

    def show_all_data(self):
        
        st.title("Visualização de Dados Estruturados")
        st.dataframe(self.df_structured)
        st.write("### Informações Gerais")
        st.write(self.df_structured.describe())
        st.title("Visualização de Dados Não Estruturados")
        st.dataframe(self.df_no_structured)
        st.write("### Informações Gerais")
        st.write(self.df_no_structured.describe())
        if st.button("Enviar mensagem"):
            MessagePublisher(self.worksheet_structured, self.worksheet_no_structured).publish_message()

