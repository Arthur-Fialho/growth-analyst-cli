# Growth-Analyst AI-Native CLI

🌐 **Select Language / Selecione o Idioma**
- [English (EN)](#english)
- [Português (PT-BR)](#portugues)

---

<a id="english"></a>
# Growth-Analyst AI-Native CLI (English)

An autonomous Python Command Line Interface (CLI) to process A/B test datasets for cashback variations. It generates detailed aggregate metrics, utilizes the user's preferred LLM provider (OpenAI, Anthropic, or Gemini) to perform a professional growth/sustainability analysis with structured JSON output, logs the test results to a centralized Google Sheet (with a local CSV fallback), and creates professional local Markdown and HTML reports.

## 📋 Table of Contents
1. [🛠️ Setup & Installation](#setup-and-installation)
2. [✨ Features](#features)
3. [🤖 The AI-Native Workflow (Natural Language Execution)](#ai-native-workflow)
4. [🚀 How to Run (Traditional CLI)](#how-to-run)

---

<a id="setup-and-installation"></a>
## 🛠️ Setup & Installation

### 1. Clone the Repository & Navigate to the Folder
Clone the repository using Git and navigate to the project directory:
*   **Via HTTPS:**
    ```bash
    git clone https://github.com/Arthur-Fialho/growth-analyst-cli.git
    cd growth-analyst-cli
    ```
*   **Via SSH:**
    ```bash
    git clone git@github.com:Arthur-Fialho/growth-analyst-cli.git
    cd growth-analyst-cli
    ```

### 2. Open in Antigravity or Claude Code
Open the project folder in your preferred AI-native environment:
*   **Antigravity (IDE)**: Open the cloned folder `growth-analyst-cli` directly in the Antigravity IDE.
*   **Claude Code**: Start Claude Code inside the project directory in your terminal:
    ```bash
    claude
    ```

### 3. Requirements
Ensure you have Python 3.8+ installed.

### 4. Install Dependencies
Install the required packages using pip:
```bash
pip install -r requirements.txt
```
*Note: If your system uses PEP 668 (externally managed environment), you can install them using `--break-system-packages` flag:*
```bash
pip install --break-system-packages -r requirements.txt
```

### 5. Environment Variables (.env)
Create a `.env` file in the root of the project (copy from `.env.example`) and configure your preferred AI provider API key along with sheets tracking:
```env
# AI Providers (Fill the one you want to use; OpenAI is prioritized, then Anthropic, then Gemini fallback)
OPENAI_API_KEY="your-openai-api-key"
ANTHROPIC_API_KEY="your-anthropic-api-key"
GEMINI_API_KEY="your-gemini-api-key"

# central Google Sheets tracking config
GOOGLE_SHEET_ID="your-google-sheet-id"
GOOGLE_SHEETS_CREDENTIALS_JSON="your-raw-json-credentials-string"

# Optional Gemini model override
GEMINI_MODEL="gemini-2.5-flash"
```

### 6. Google Sheets Integration Setup (Optional)
To receive the generated reports directly in Google Sheets, you need to configure `GOOGLE_SHEET_ID` and `GOOGLE_SHEETS_CREDENTIALS_JSON` in your `.env` file. Here is how to create and configure them:

1. **Create a Google Cloud Project**:
   - Open the [Google Cloud Console](https://console.cloud.google.com/).
   - Click on the project dropdown, select **New Project**, name it (e.g. `growth-analyst-cli`), and click **Create**.
2. **Enable APIs**:
   - Go to **APIs & Services > Library**.
   - Search for **Google Drive API** and click **Enable**.
   - Search for **Google Sheets API** and click **Enable**.
3. **Create a Service Account & Download Credentials JSON**:
   - Go to **APIs & Services > Credentials**.
   - Click **+ Create Credentials** and choose **Service Account**.
   - Enter a service account name, click **Create and Continue**, then click **Done**.
   - In the Service Accounts list, click on the newly created service account's email.
   - Go to the **Keys** tab, click **Add Key > Create new key**, select **JSON**, and click **Create**.
   - A JSON file will be downloaded. Open it, copy the entire JSON string, and paste it into the `GOOGLE_SHEETS_CREDENTIALS_JSON` variable inside your `.env` (ensure it is placed within single or double quotes, e.g. `GOOGLE_SHEETS_CREDENTIALS_JSON='{...}'`).
4. **Configure Google Sheet ID**:
   - Create a new Google Spreadsheet or open an existing one.
   - Share the spreadsheet with the Service Account email (e.g., `your-service-account@...gserviceaccount.com`) as an **Editor**.
   - Copy the spreadsheet ID from the browser URL (the part between `/d/` and `/edit`).
   - Paste this ID into the `GOOGLE_SHEET_ID` variable in your `.env`.


---

<a id="features"></a>
## ✨ Features

- **Module A: Data Sanitization (Pandas)**: Cleans Brazilian formatted currency strings (R$), drops invalid rows, groups by variant, and calculates aggregate growth/financial metrics. Also implements **Smart Data Routing** to automatically copy outside CSVs to the local `data/` directory.
- **Module B: AI Analyzer (Multi-Model Support)**: Sends aggregate metrics to your chosen AI provider (OpenAI `gpt-4o-mini`, Anthropic `claude-3-5-sonnet-latest`, or Gemini `gemini-2.5-flash`) using priority-based environment variables. Enforces structured JSON output parsing to keep other modules fully compatible and vendor-lock-in free.
- **Module C: Storage & Tracking (Google Sheets API)**: Registers analysis in a centralized sheet using `gspread`, falling back gracefully to a local `result_sheet.csv` if credentials/connection fail.
- **Module D: Presentation Layer**: Generates detailed local Markdown reports (for developer/agent parsing) and beautifully styled HTML reports (for managers/directors) under `reports/`, prints a summary layout to the console, and displays a clickable local file:// URI.

---

<a id="ai-native-workflow"></a>
## 🤖 The AI-Native Workflow (Natural Language Execution)

This CLI is designed to be agent-friendly. **You do not need to memorize terminal commands or type CLI options manually.** You can execute analyses entirely through natural language by dropping a CSV file into Cursor, Claude Code, or other AI assistants.

### How to interact via natural language:
1. **Drop or Attach**: Drag and drop or attach your CSV file into the AI chat interface (Cursor Composer, Claude Code, etc.).
   *Note: If you cannot drag/attach the CSV file directly into the AI agent's chat window, simply place the CSV file anywhere in the project folder (ideally in the `data/` folder or at the project root). The CLI's Smart Data Routing will automatically locate the file, copy it to the `data/` directory for organization, and run the pipeline. Just ask the AI to analyze the file `yourfilename.csv` or its project path.*
2. **Ask in Natural Language**:
   > *"Analyze this dataset for me"* or *"Analyze the A/B test of Partner A at data/dataset_01_parceiroA.csv"*
3. **Execution**: The AI agent will read the `.cursorrules` and `README.md` files, automatically execute `python main.py <path_to_file>` (handling Smart Data Routing if the file was outside the project), parse the output, and present the final Growth decision directly in your chat window.

---

<a id="how-to-run"></a>
## 🚀 How to Run (Traditional CLI)

Analyze a dataset by specifying the path to the CSV:
```bash
python3 main.py data/dataset_01_parceiroA.csv
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

Uma interface de linha de comando (CLI) em Python para processar dados de testes A/B de variações de cashback. Ela calcula métricas agregadas, utiliza o provedor de IA de sua escolha (OpenAI, Anthropic ou Gemini) para realizar uma análise de sustentabilidade financeira sob a perspectiva de um Growth Analyst Sênior com retorno em JSON estruturado, registra os resultados em uma planilha do Google Sheets (com fallback local em CSV) e gera relatórios em Markdown e HTML.

## 📋 Tabela de Conteúdos
1. [🛠️ Instalação e Configuração](#instalacao-e-configuracao)
2. [✨ Funcionalidades](#funcionalidades)
3. [🤖 O Fluxo de Trabalho AI-Native (Execução em Linguagem Natural)](#fluxo-ai-native)
4. [🚀 Como Executar (CLI Tradicional)](#como-executar)

---

<a id="instalacao-e-configuracao"></a>
## 🛠️ Instalação e Configuração

### 1. Clonar o Repositório e Acessar a Pasta
Clone o repositório utilizando Git e navegue até a pasta do projeto:
*   **Via HTTPS:**
    ```bash
    git clone https://github.com/Arthur-Fialho/growth-analyst-cli.git
    cd growth-analyst-cli
    ```
*   **Via SSH:**
    ```bash
    git clone git@github.com:Arthur-Fialho/growth-analyst-cli.git
    cd growth-analyst-cli
    ```

### 2. Abrir no Antigravity ou Claude Code
Abra a pasta do projeto no seu ambiente de IA preferido:
*   **Antigravity (IDE)**: Abra a pasta clonada `growth-analyst-cli` diretamente na IDE Antigravity.
*   **Claude Code**: Inicie o Claude Code no seu terminal dentro do diretório do projeto:
    ```bash
    claude
    ```

### 3. Requisitos
Certifique-se de ter o Python 3.8+ instalado.

### 4. Instalar Dependências
Instale as dependências necessárias com pip:
```bash
pip install -r requirements.txt
```
*Nota: Se o seu sistema utiliza ambientes gerenciados externamente (PEP 668), use o parâmetro `--break-system-packages`:*
```bash
pip install --break-system-packages -r requirements.txt
```

### 5. Variáveis de Ambiente (.env)
Crie um arquivo `.env` na raiz do projeto (copiado de `.env.example`) e configure a chave de API do seu provedor de IA preferido:
```env
# Provedores de IA (Preencha o que deseja utilizar; OpenAI tem prioridade, seguido por Anthropic e Gemini fallback)
OPENAI_API_KEY="sua-chave-api-openai"
ANTHROPIC_API_KEY="sua-chave-api-anthropic"
GEMINI_API_KEY="sua-chave-api-gemini"

# Configurações do Google Sheets
GOOGLE_SHEET_ID="id-da-planilha-google"
GOOGLE_SHEETS_CREDENTIALS_JSON="conteudo-json-de-credenciais-de-conta-de-servico"

# Opcional (override do modelo Gemini)
GEMINI_MODEL="gemini-2.5-flash"
```

### 6. Configuração da Integração com o Google Sheets (Opcional)
Para enviar os relatórios gerados diretamente para uma planilha do Google Sheets, você precisa configurar as variáveis `GOOGLE_SHEET_ID` e `GOOGLE_SHEETS_CREDENTIALS_JSON` no seu arquivo `.env`. Veja como criar e configurar as credenciais:

1. **Criar um Projeto no Google Cloud**:
   - Acesse o [Google Cloud Console](https://console.cloud.google.com/).
   - Clique no seletor de projetos, clique em **Novo Projeto**, dê um nome (por exemplo, `growth-analyst-cli`) e clique em **Criar**.
2. **Habilitar APIs**:
   - Acesse **APIs e Serviços > Biblioteca**.
   - Pesquise por **Google Drive API** e clique em **Ativar**.
   - Pesquise por **Google Sheets API** e clique em **Ativar**.
3. **Criar Conta de Serviço e Baixar Credenciais JSON**:
   - Acesse **APIs e Serviços > Credenciais**.
   - Clique em **+ Criar Credenciais** e selecione **Conta de serviço**.
   - Preencha o nome da conta de serviço, clique em **Criar e Continuar** e depois em **Concluir**.
   - Na lista de Contas de Serviço, clique no e-mail da conta que acabou de criar.
   - Vá para a aba **Chaves**, clique em **Adicionar chave > Criar nova chave**, selecione **JSON** e clique em **Criar**.
   - Um arquivo JSON será baixado. Abra-o, copie todo o conteúdo e cole-o na variável `GOOGLE_SHEETS_CREDENTIALS_JSON` do seu `.env` (certifique-se de colocá-lo entre aspas simples, ex: `GOOGLE_SHEETS_CREDENTIALS_JSON='{...}'`).
4. **Configurar o ID da Planilha**:
   - Crie ou abra uma planilha no Google Sheets.
   - Compartilhe a planilha com o e-mail da Conta de Serviço (ex: `seu-email-da-conta-de-servico@...gserviceaccount.com`) dando permissão de **Editor**.
   - Copie o ID da planilha contido na URL do navegador (a parte entre `/d/` e `/edit`).
   - Cole esse ID na variável `GOOGLE_SHEET_ID` no seu `.env`.


---

<a id="funcionalidades"></a>
## ✨ Funcionalidades

- **Módulo A: Higienização de Dados (Pandas)**: Limpa valores monetários brasileiros (R$), remove linhas corrompidas e calcula agregados financeiros e de ROI por grupo. Também implementa o **Roteamento de Dados Inteligente** para copiar automaticamente CSVs externos para a pasta `data/`.
- **Módulo B: AI Analyzer (Suporte Multi-Modelo)**: Envia métricas agregadas para o provedor de IA de sua escolha (OpenAI `gpt-4o-mini`, Anthropic `claude-3-5-sonnet-latest` ou Gemini `gemini-2.5-flash`) de forma agnóstica a fornecedores. Garante a saída no mesmo esquema JSON para compatibilidade total.
- **Módulo C: Armazenamento e Rastreamento (Google Sheets)**: Registra o teste em uma planilha compartilhada usando `gspread` com fallback automático em arquivo `result_sheet.csv`.
- **Módulo D: Apresentação**: Gera relatórios Markdown locais (para desenvolvedores/agentes de IA) e relatórios HTML com estilização profissional corporativa (para gerentes/diretores) na pasta `reports/`, exibe um sumário no terminal e fornece uma URI clicável file:// para abrir o relatório HTML no navegador.

---

<a id="fluxo-ai-native"></a>
## 🤖 O Fluxo de Trabalho AI-Native (Execução em Linguagem Natural)

Esta CLI foi projetada para ser amigável para agentes de IA. **Você não precisa memorizar comandos de terminal ou digitar opções da CLI manualmente.** Você pode executar análises inteiramente usando linguagem natural simplesmente arrastando e soltando um arquivo CSV no Cursor, Claude Code ou outro assistente de IA.

### Como interagir via linguagem natural:
1. **Arrastar e Anexar**: Arraste e solte ou anexe seu arquivo CSV na interface de chat da IA (Cursor Composer, Claude Code, etc.).
   *Nota: Se não for possível arrastar/anexar o arquivo CSV diretamente na caixa de texto do agente de IA, basta colocar o arquivo em qualquer pasta do projeto (idealmente dentro da pasta `data/` ou na raiz do projeto). O Roteamento Inteligente de Dados da CLI irá localizá-lo, copiá-lo para a pasta `data/` para manter a organização e executar a análise. Em seguida, basta pedir para a IA analisar o arquivo `nome_do_arquivo.csv` ou indicar o seu caminho.*
2. **Pergunte em Linguagem Natural**:
   > *"Analise este dataset para mim"* ou *"Analise o teste A/B do Parceiro A em data/dataset_01_parceiroA.csv"*
3. **Execução**: O agente de IA lerá as regras em `.cursorrules` e `README.md`, executará automaticamente `python main.py <caminho_do_arquivo>` (copiando-o para a pasta `data/` se necessário), processará a saída e apresentará a decisão final de Growth diretamente na sua tela de chat.

---

<a id="como-executar"></a>
## 🚀 Como Executar (CLI Tradicional)

Execute a análise passando o caminho do arquivo CSV:
```bash
python3 main.py data/dataset_01_parceiroA.csv
```

*Nota: Com o Roteamento de Dados Inteligente (Smart Data Routing), se você especificar um arquivo CSV fora do diretório do projeto, a CLI o copiará automaticamente para a pasta `data/` para manter o repositório organizado.*

### Opções:
- `--sheet-id [ID]`: Sobrescreve o ID da planilha do Google.
- `--test-name "[Nome]"`: Define um nome customizado para o teste.
- `--test-description "[Descrição]"`: Define uma descrição customizada para o teste.