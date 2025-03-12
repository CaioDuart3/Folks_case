from decouple import config
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import torch
import os
torch.classes.__path__ = []


credentials_path = os.path.join(os.path.dirname(__file__), config("SERVICE_ACCOUNT") ) #tranforma em string o caminho para as credênciais

class GoogleSheetsClient:
    """
    Se conecta as APIs Google Sheet e Google Drive, para que possa modificar as planilhas na Web,
    de forma que proteja os dados sensíveis contidos nas planilhas

    Recebe como argumento o arquivo credentials_path que contém a autenticação ecessária com a API
    """
    def __init__(self, filename:str):
        self.__filename = filename # para autenticar com a API
        self.scopes = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive",
        ]
        self.client = self._authenticate()

    def _authenticate(self):
        """ autentica com as APIs"""
        creds = ServiceAccountCredentials.from_json_keyfile_name(self.__filename, self.scopes)
        return gspread.authorize(creds)

    def get_data(self, spreadsheet_title:str, folder_id:str) -> gspread.worksheet.Worksheet:
        """ Retorna a planilha no formato do gspread, formato este útil para a manipulação e atualização na Web"""

        sheet = self.client.open(title=spreadsheet_title, folder_id=folder_id) # Retorna toda planilha com N páginas
        worksheet = sheet.get_worksheet(0) # Retorna somente a primeira página da planilha com N páginas
        return worksheet
    

def get_data_worksheet(title: str, folder_id: str) -> gspread.worksheet.Worksheet:
    """ Conecta com as APIs do Google Sheet e  Google Drive e extrai a primeira página da planilha """

    googleSheet = GoogleSheetsClient(credentials_path)
    wk = googleSheet.get_data(
        spreadsheet_title=title,
        folder_id=folder_id
    )
    return wk




