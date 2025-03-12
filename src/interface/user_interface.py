

from interface.ui_send_message import SendMessageInterface
from interface.authenticator import Authenticator
from typing import Optional
from decouple import config
import pandas as pd
import streamlit as st
import gspread
import torch

torch.classes.__path__ = []


class UserInterface:
    """Monta a interface para o usuário no Streamlit"""
    
    def __init__(self, worksheet_structured: Optional[gspread.worksheet.Worksheet], worksheet_no_structured: Optional[gspread.worksheet.Worksheet]):
        self.worksheet_structured = worksheet_structured
        self.worksheet_no_structured = worksheet_no_structured
        self.df_structured = self._get_dataframe(self.worksheet_structured)
        self.df_no_structured = self._get_dataframe(self.worksheet_no_structured)
        self.authenticator = Authenticator(config("USERNAME_STREAMLIT"), config("PASSWORD_STREAMLIT"))
        
    def _get_dataframe(self, worksheet: Optional[gspread.worksheet.Worksheet]) -> pd.DataFrame:
        """
            Retorna o dataFrame do objeto gspread,
            dataFrames são úteis para mostrar os dados no streamlit, pois o mesmo tem suporte a este tipo de dado
        """

        if worksheet is not None:
            records = worksheet.get_all_records()
            return pd.DataFrame(records) if records else pd.DataFrame()
        return pd.DataFrame()

    def display_data(self):
        """ inicializa a interface principal """

        if self.authenticator.authenticate():
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
        """ Mostra os dados estruturados quando filtrado pelo mesmo"""
        st.title("Visualização de Dados Estruturados")
        st.dataframe(self.df_structured)
        st.write("### Informações Gerais")
        st.write(self.df_structured.describe())

        if st.button("Enviar mensagem"):
            SendMessageInterface(self.worksheet_structured, None).publish_message()

    def show_no_structured_data(self):
        """ Mostra os dados NÃO estruturados quando filtrado pelo mesmo"""
        st.title("Visualização de Dados Não Estruturados")
        st.dataframe(self.df_no_structured)
        st.write("### Informações Gerais")
        st.write(self.df_no_structured.describe())

        if st.button("Enviar mensagem"):
            SendMessageInterface(None, self.worksheet_no_structured).publish_message()

    def show_all_data(self):
        """ Mostra todos os dados quando filtrado pelo mesmo"""
        st.title("Visualização de Dados Estruturados")
        st.dataframe(self.df_structured)
        st.write("### Informações Gerais")
        st.write(self.df_structured.describe())
        st.title("Visualização de Dados Não Estruturados")
        st.dataframe(self.df_no_structured)
        st.write("### Informações Gerais")
        st.write(self.df_no_structured.describe())

        if st.button("Enviar mensagem"):
            SendMessageInterface(self.worksheet_structured, self.worksheet_no_structured).publish_message()
