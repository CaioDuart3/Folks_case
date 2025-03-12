from decouple import config
from services.google_sheets import get_data_worksheet
from interface.user_interface import UserInterface
import torch
import logging

# Evita o Pytorch procurar pacotes e módulos não essenciais
torch.classes.__path__ = []

# Configuração de log
logging.basicConfig(level=logging.INFO)

def main():
    try:
        # Carregar as planilhas
        spreadsheet_title_structured = config("SPREADSHEET_TITLE_STRUCTURED")
        spreadsheet_title_no_structured = config("SPREADSHEET_TITLE_NO_STRUCTURED")
        folder_id = config("FOLDER_ID")
        
        logging.info(f"Carregando planilha estruturada: {spreadsheet_title_structured}")
        worksheet_structured = get_data_worksheet(spreadsheet_title_structured, folder_id)
        
        logging.info(f"Carregando planilha não estruturada: {spreadsheet_title_no_structured}")
        worksheet_no_structured = get_data_worksheet(spreadsheet_title_no_structured, folder_id)

        # Inicializar a interface de usuário
        viewer = UserInterface(worksheet_structured, worksheet_no_structured)
        viewer.display_data()

    except Exception as e:
        logging.error(f"Erro ao carregar as planilhas ou iniciar a interface: {str(e)}")

if __name__ == "__main__":
    main()
