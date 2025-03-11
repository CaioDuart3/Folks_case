from decouple import config
from services.googleSheets import *
from streamlit_app.dataViewer import *
import torch

# Evita o Pytorch procure pacotes e módulos não essenciais para aplicação
torch.classes.__path__ = []

if __name__ == "__main__":
    worksheet_structured = get_data_worksheet(config("SPREADSHEET_TITLE_STRUCTURED"), config("FOLDER_ID"))
    worksheet_no_structured = get_data_worksheet(config("SPREADSHEET_TITLE_NO_STRUCTURED"), config("FOLDER_ID"))
    viewer = DataViewer(worksheet_structured, worksheet_no_structured)
    viewer.display_data()
