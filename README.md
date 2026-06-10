# Growth-Analyst AI-Native CLI

An autonomous Python Command Line Interface (CLI) to process A/B test datasets for cashback variations. It generates detailed aggregate metrics, utilizes the Google Gemini API to perform a professional growth/sustainability analysis with structured JSON output, logs the test results to a centralized Google Sheet (with a local CSV fallback), and creates professional local Markdown reports.

---

## Features

- **Module A: Data Sanitization (Pandas)**: Cleans Brazilian formatted currency strings (R$), drops invalid rows, groups by variant, and calculates aggregate growth/financial metrics.
- **Module B: AI Analyzer (Gemini API)**: Sends aggregate data to Gemini to act as a Senior Growth Analyst and returns structured JSON analysis.
- **Module C: Storage & Tracking (Google Sheets API)**: Registers analysis in a centralized sheet using `gspread`, falling back gracefully to a local `result_sheet.csv` if credentials/connection fail.
- **Module D: Presentation Layer**: Generates detailed local Markdown reports under `reports/` and prints a summary layout to the console.

---

## Setup & Installation

### 1. Requirements
Ensure you have Python 3.8+ installed.

### 2. Install Dependencies
Install the required packages using pip:
```bash
pip install -r requirements.txt
```
*Note: If your system uses PEP 668 (externally managed environment), you can install them using `--break-system-packages` flag:*
```bash
pip install --break-system-packages -r requirements.txt
```

### 3. Environment Variables (.env)
Create a `.env` file in the root of the project (copy from `.env.example`) and configure the following variables:
```env
GEMINI_API_KEY="your-gemini-api-key"
GOOGLE_SHEET_ID="your-google-sheet-id"
GOOGLE_SHEETS_CREDENTIALS_JSON="your-raw-json-credentials-string"
```

---

## How to Run

Analyze a dataset by specifying the path to the CSV:
```bash
python main.py data/dataset_01_parceiroA.csv
```

### Options:
- `--sheet-id [ID]`: Override the target Google Sheet ID.
- `--test-name "[Name]"`: Customize the name of the test.
- `--test-description "[Description]"`: Customize the description of the test.

---
---

# Growth-Analyst AI-Native CLI (Português)

Uma interface de linha de comando (CLI) em Python para processar dados de testes A/B de variações de cashback. Ela calcula métricas agregadas, utiliza a API do Google Gemini para realizar uma análise de sustentabilidade financeira sob a perspectiva de um Growth Analyst Sênior com retorno em JSON estruturado, registra os resultados em uma planilha do Google Sheets (com fallback local em CSV) e gera relatórios em Markdown.

---

## Funcionalidades

- **Módulo A: Higienização de Dados (Pandas)**: Limpa valores monetários brasileiros (R$), remove linhas corrompidas e calcula agregados financeiros e de ROI por grupo.
- **Módulo B: AI Analyzer (API Gemini)**: Envia os agregados ao modelo Gemini para análise sob a perspectiva de um analista de growth com saída em formato JSON.
- **Módulo C: Armazenamento e Rastreamento (Google Sheets)**: Registra o teste em uma planilha compartilhada usando `gspread` com fallback automático em arquivo `result_sheet.csv`.
- **Módulo D: Apresentação**: Gera relatórios Markdown locais na pasta `reports/` e exibe um sumário no terminal.

---

## Instalação e Configuração

### 1. Requisitos
Certifique-se de ter o Python 3.8+ instalado.

### 2. Instalar Dependências
Instale as dependências necessárias com pip:
```bash
pip install -r requirements.txt
```
*Nota: Se o seu sistema utiliza ambientes gerenciados externamente (PEP 668), use o parâmetro `--break-system-packages`:*
```bash
pip install --break-system-packages -r requirements.txt
```

### 3. Variáveis de Ambiente (.env)
Crie um arquivo `.env` na raiz do projeto (copiado de `.env.example`):
```env
GEMINI_API_KEY="sua-chave-api-gemini"
GOOGLE_SHEET_ID="id-da-planilha-google"
GOOGLE_SHEETS_CREDENTIALS_JSON="conteudo-json-de-credenciais-de-conta-de-servico"
```

---

## Como Executar

Execute a análise passando o caminho do arquivo CSV:
```bash
python main.py data/dataset_01_parceiroA.csv
```

### Opções:
- `--sheet-id [ID]`: Sobrescreve o ID da planilha do Google.
- `--test-name "[Nome]"`: Define um nome customizado para o teste.
- `--test-description "[Descrição]"`: Define uma descrição customizada para o teste.