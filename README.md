# Tutorial Completo de Como Executar o Sistema

Este tutorial irá guiá-lo na configuração e execução de um projeto Python que integra as APIs do Google Sheets e Google Drive para manipulação de dados de planilhas, e utiliza RabbitMQ para enviar mensagens via WhatsApp.

## Funcionalidades do Projeto

- **Integração com Google Sheets e Google Drive:** O sistema lê dados de planilhas públicas ou privadas utilizando a APIs do Google.

- **Análise de Dados:** A análise é feita para identificar quais clientes estão aptos a receber mensagens, com base no código TUSS ou com o uso da IA.

- **BioBERT**, que analisa receitas médicas.

- **Envio de Mensagens via WhatsApp:** Após a filtragem, o sistema envia mensagens aos clientes aptos utilizando RabbitMQ para orquestrar o processo de envio.

- **Armazenamento de Dados:** O status do envio de mensagens e os registros são salvos diretamente nas planilhas do Google, permitindo análise posterior no Streamlit e no Looker Studio com dashboard interativas.

## Tecnologias Utilizadas

- **Python:** Linguagem principal para a lógica do sistema.
- **Google Sheets API:** Para leitura e escrita de dados em planilhas do Google Sheets.
- **Google Drive API:** Para manipulação de arquivos armazenados no Google Drive.
- **RabbitMQ:** Para orquestrar o envio de mensagens de forma assíncrona.
- **Docker:** Para empacotar o RabbitMQ.
- **Streamlit:** Para criar uma interface simples e visualização dos dados do sistema.

## Pré-requisitos

Antes de rodar o projeto, verifique se você tem os seguintes pré-requisitos instalados:

- **Docker:** Para executar o projeto em um contêiner. [Documentação do Docker](https://docs.docker.com/get-started/).
- **Python 3.12 ou superior:** Para rodar o código Python. [Documentação do Python](https://docs.python.org/pt-br/3/).
- **Pip:** Gerenciador de pacotes do Python. [Guia de instalação do Pip e ambientes virtuais](https://packaging.python.org/pt-br/latest/guides/installing-using-pip-and-virtual-environments/).
- **Conta do Google com permissões de acesso às APIs do Google Sheets e Google Drive:** [Como obter a conta do Google com permissões?](https://youtu.be/6XaF4ZF7LW0?feature=shared&t=530).
- **RabbitMQ:** Para orquestrar o envio de mensagens. [Como instalar o RabbitMQ?](https://youtu.be/6XaF4ZF7LW0?feature=shared&t=530).

## Passo a Passo: Como Configurar o Projeto

### Passo 1: Clone o Repositório

Primeiro, clone o repositório do projeto para sua máquina local:

```bash
git clone https://github.com/usuario/projeto.git
cd projeto
```
### Passo 2: Criação dos Arquivos de Configuração

No diretório raiz do projeto, adicione os seguintes arquivos para configurar o sistema:

1. **Arquivo `.env`**: Contém as variáveis de ambiente necessárias para a configuração do projeto.
2. **Arquivo `credentials/sua-api-key.json`**: Este arquivo contém as credenciais da conta de serviço da google com acesso para as APIs do Google.

#### Exemplo de configuração do `.env`:

```ini
# Planilha de códigos TUSS, utilizada para filtrar dados
REFERENCE_SPREADSHEET = https://docs.google.com/spreadsheets/d/1myt01dskR0tjmNSCLgM5bigshHsJNsUzxyFIbMTUA_M/export?format=csv

# Google API
SERVICE_ACCOUNT = ../../credentials/sua-api-key.json  # Caminho para o arquivo de credenciais
SPREADSHEET_TITLE_STRUCTURED = sample_estruturados   # Título da planilha de dados estruturados
SPREADSHEET_TITLE_NO_STRUCTURED = sample_nao_estruturados  # Título da planilha de dados não estruturados
FOLDER_ID = 123456789abc123456789abc  # ID da pasta no Google Drive
DATA_VIEW_LINK = https://lookerstudio.google.com/reporting/12345  # Link da dashboard do Looker Studio

# Mensageria com RabbitMQ
RABBITMQ_QUEUE = sua_fila  # Nome da fila no RabbitMQ
RABBITMQ_HOST = localhost
RABBITMQ_PORT = 5672  # Porta padrão do RabbitMQ
RABBITMQ_USER = guest  # Usuário do RabbitMQ
RABBITMQ_PASSWORD = guest  # Senha do RabbitMQ
RABBITMQ_EXCHANGE = sua_exchange
RABBITMQ_ROUTING_KEY = sua_routing_key

# Autenticação no Streamlit
USERNAME_STREAMLIT = guest  # Usuário do Streamlit
PASSWORD_STREAMLIT = guest  # Senha do Streamlit
```
Como consigo a `credentials/sua-api-key.json`? Siga o tutotial: https://youtu.be/6XaF4ZF7LW0?feature=shared&t=530

### Passo 3: Criando e Ativando o Ambiente Virtual

Agora, vamos criar um ambiente virtual Python para garantir que as dependências do projeto sejam isoladas e não interfiram no sistema global.

1. **Criação do ambiente virtual:**

Execute o comando abaixo para criar o ambiente virtual:
```bash
python3 -m venv .venv
```
Para rodar o ambiente virtual utilize:
``` bash
# No linux/MacOS
source venv/bin/activate
# No windows:
.venv\Scripts\activate

```
Após isso, insira este comando ainda na raiz do projeto para baixar as dependências do sistema:

``` bash
pip install -r requirements.txt
```

### Passo4 - Executar o projeto
Para executar o projeto e visualizar pela interface gráfica do streamlit utilize o comando:
``` bash
streamlit run src/app.py
```
Agora você pode acessar a interface pelo servidor: http://localhost:8501/


