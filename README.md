# Growth-Analyst AI-Native CLI

🌐 **Select Language / Selecione o Idioma**
- [English (EN)](#english)
- [Português (PT-BR)](#portugues)

---

<a id="english"></a>
# Growth-Analyst AI-Native CLI (English)

An autonomous Python Command Line Interface (CLI) to process A/B test datasets for cashback variations. It generates detailed aggregate metrics, utilizes the Google Gemini API to perform a professional growth/sustainability analysis with structured JSON output, logs the test results to a centralized Google Sheet (with a local CSV fallback), and creates professional local Markdown reports.

## 📋 Table of Contents
1. [🛠️ Setup & Installation](#%EF%B8%8F-setup--installation)
2. [✨ Features](#-features)
3. [🤖 The AI-Native Workflow (Natural Language Execution)](#-the-ai-native-workflow-natural-language-execution)
4. [🚀 How to Run (Traditional CLI)](#-how-to-run-traditional-cli)

---

## 🛠️ Setup & Installation

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

## ✨ Features

- **Module A: Data Sanitization (Pandas)**: Cleans Brazilian formatted currency strings (R$), drops invalid rows, groups by variant, and calculates aggregate growth/financial metrics. Also implements **Smart Data Routing** to automatically copy outside CSVs to the local `data/` directory.
- **Module B: AI Analyzer (Gemini API)**: Sends aggregate data to Gemini to act as a Senior Growth Analyst and returns structured JSON analysis.
- **Module C: Storage & Tracking (Google Sheets API)**: Registers analysis in a centralized sheet using `gspread`, falling back gracefully to a local `result_sheet.csv` if credentials/connection fail.
- **Module D: Presentation Layer**: Generates detailed local Markdown reports under `reports/` and prints a summary layout to the console.

---

## 🤖 The AI-Native Workflow (Natural Language Execution)

This CLI is designed to be agent-friendly. **You do not need to memorize terminal commands or type CLI options manually.** You can execute analyses entirely through natural language by dropping a CSV file into Cursor, Claude Code, or other AI assistants.

### How to interact via natural language:
1. **Drop or Attach**: Drag and drop or attach your CSV file into the AI chat interface (Cursor Composer, Claude Code, etc.).
2. **Ask in Natural Language**:
   > *"Analyze this dataset for me"* or *"Analyze the A/B test of Partner A at data/dataset_01_parceiroA.csv"*
3. **Execution**: The AI agent will read the `.cursorrules` and `README.md` files, automatically execute `python main.py <path_to_file>` (handling Smart Data Routing if the file was outside the project), parse the output, and present the final Growth decision directly in your chat window.

---

## 🚀 How to Run (Traditional CLI)

Analyze a dataset by specifying the path to the CSV:
```bash
python main.py data/dataset_01_parceiroA.csv
```

*Note: With Smart Data Routing, if you specify a CSV file from outside the project directory, the CLI will automatically copy it into the `data/` folder for repository organization.*

### Options:
- `--sheet-id [ID]`: Override the target Google Sheet ID.
- `--test-name "[Name]"`: Customize the name of the test.
- `--test-description "[Description]"`: Customize the description of the test.

<br>
<br>

<div align="center">
  <p>====================================================================================</p>
  <h2>🔄 End of English Section / Fim da Seção em Inglês 🔄</h2>
  <p>====================================================================================</p>
</div>

<br>
<br>

---

<a id="portugues"></a>
# Growth-Analyst AI-Native CLI (Português)

Uma interface de linha de comando (CLI) em Python para processar dados de testes A/B de variações de cashback. Ela calcula métricas agregadas, utiliza a API do Google Gemini para realizar uma análise de sustentabilidade financeira sob a perspectiva de um Growth Analyst Sênior com retorno em JSON estruturado, registra os resultados em uma planilha do Google Sheets (com fallback local em CSV) e gera relatórios em Markdown.

## 📋 Tabela de Conteúdos
1. [🛠️ Instalação e Configuração](#%EF%B8%8F-instalacao-e-configuracao)
2. [✨ Funcionalidades](#-funcionalidades)
3. [🤖 O Fluxo de Trabalho AI-Native (Execução em Linguagem Natural)](#-o-fluxo-de-trabalho-ai-native-execucao-em-linguagem-natural)
4. [🚀 Como Executar (CLI Tradicional)](#-como-executar-cli-tradicional)

---

## 🛠️ Instalação e Configuração

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

## ✨ Funcionalidades

- **Módulo A: Higienização de Dados (Pandas)**: Limpa valores monetários brasileiros (R$), remove linhas corrompidas e calcula agregados financeiros e de ROI por grupo. Também implementa o **Roteamento de Dados Inteligente** para copiar automaticamente CSVs externos para a pasta `data/`.
- **Módulo B: AI Analyzer (API Gemini)**: Envia os agregados ao modelo Gemini para análise sob a perspectiva de um analista de growth com saída em formato JSON.
- **Módulo C: Armazenamento e Rastreamento (Google Sheets)**: Registra o teste em uma planilha compartilhada usando `gspread` com fallback automático em arquivo `result_sheet.csv`.
- **Módulo D: Apresentação**: Gera relatórios Markdown locais na pasta `reports/` e exibe um sumário no terminal.

---

## 🤖 O Fluxo de Trabalho AI-Native (Execução em Linguagem Natural)

Esta CLI foi projetada para ser amigável para agentes de IA. **Você não precisa memorizar comandos de terminal ou digitar opções da CLI manualmente.** Você pode executar análises inteiramente usando linguagem natural simplesmente arrastando e soltando um arquivo CSV no Cursor, Claude Code ou outro assistente de IA.

### Como interagir via linguagem natural:
1. **Arrastar e Anexar**: Arraste e solte ou anexe seu arquivo CSV na interface de chat da IA (Cursor Composer, Claude Code, etc.).
2. **Pergunte em Linguagem Natural**:
   > *"Analise este dataset para mim"* ou *"Analise o teste A/B do Parceiro A em data/dataset_01_parceiroA.csv"*
3. **Execução**: O agente de IA lerá as regras em `.cursorrules` e `README.md`, executará automaticamente `python main.py <caminho_do_arquivo>` (copiando-o para a pasta `data/` se necessário), processará a saída e apresentará a decisão final de Growth diretamente na sua tela de chat.

---

## 🚀 Como Executar (CLI Tradicional)

Execute a análise passando o caminho do arquivo CSV:
```bash
python main.py data/dataset_01_parceiroA.csv
```

*Nota: Com o Roteamento de Dados Inteligente (Smart Data Routing), se você especificar um arquivo CSV fora do diretório do projeto, a CLI o copiará automaticamente para a pasta `data/` para manter o repositório organizado.*

### Opções:
- `--sheet-id [ID]`: Sobrescreve o ID da planilha do Google.
- `--test-name "[Nome]"`: Define um nome customizado para o teste.
- `--test-description "[Descrição]"`: Define uma descrição customizada para o teste.