
from typing import Optional
import gspread

class WorksheetUpdater:
    """Atualiza as planilhas com o status das mensagens enviadas"""
    
    def __init__(self, worksheet: Optional[gspread.worksheet.Worksheet]):
        self.worksheet = worksheet
    
    def update(self, batch_update_data: list):
        if self.worksheet and batch_update_data:
            self.worksheet.batch_update(batch_update_data)
