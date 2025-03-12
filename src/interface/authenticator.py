import streamlit as st
class Authenticator:
    """Gerencia a autenticação do usuário na interface do Streamlit"""
    
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def authenticate(self) -> bool:
        # retorna True se os dados inseridos nos inputs forem iguais
        username_input = st.text_input("Usuário")
        password_input = st.text_input("Senha", type="password")
        return username_input == self.username and password_input == self.password
