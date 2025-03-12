import pandas as pd
from decouple import config

class DataProcessor:
    """Processa dados estruturados e não estruturados aplicando filtros"""
    
    @staticmethod
    def filter_data_for_tuss(dataframe: pd.DataFrame) -> pd.DataFrame:
        sheet_url = config("REFERENCE_SPREADSHEET")
        tuss_worksheet = pd.read_csv(sheet_url)
        tuss_codes = tuss_worksheet['TUSS'].astype(str).tolist()
        return dataframe[dataframe['CD_TUSS'].apply(lambda x: str(x) in tuss_codes)]
