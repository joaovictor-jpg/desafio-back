# 📧 API de Classificação Inteligente de Emails

Este projeto é uma solução de Backend desenvolvida para automatizar a triagem de emails corporativos. Utilizando Inteligência Artificial moderna, o sistema classifica mensagens recebidas e sugere respostas automáticas, otimizando o fluxo de trabalho de equipes de atendimento.

## 🚀 Funcionalidades

1.  **Classificação Automática:** Identifica se um email é **Produtivo** (requer ação/suporte) ou **Improdutivo** (agradecimentos/spam).
2.  **Geração de Respostas:** Utiliza LLM (Google Gemini) para redigir uma resposta contextualizada e empática.
3.  **API REST:** Endpoints prontos para integração com interfaces Web (Frontend).

## 🧠 Arquitetura e Decisões Técnicas (NLP)

O projeto foi construído em **Python** utilizando o framework **Flask**.

### Processamento de Linguagem Natural (NLP)
Para atender aos requisitos de NLP com a máxima eficácia, adotamos uma abordagem híbrida:

* **Classificação (Transformers):** Utilizamos o modelo `distilbert-base-uncased`. Diferente de abordagens clássicas (Bag of Words), optamos por **não remover stop-words ou realizar stemming agressivo** no pipeline principal. Isso ocorre porque modelos baseados em Transformers dependem do contexto semântico completo da frase para determinar a intencionalidade correta. O pré-processamento (tokenização e normalização) é realizado pelo Tokenizer nativo do modelo.
* **Geração (GenAI):** Utilizamos o modelo **Google Gemini 1.5 Flash** (via API `google-generativeai`) para gerar respostas naturais e humanizadas.
* **Legacy NLP:** O repositório contém um módulo `nlp_processor.py` com técnicas clássicas (NLTK, Lemmatização) disponível para casos de uso onde uma análise estatística simples seja necessária futuramente.

## 🛠️ Tecnologias e Bibliotecas

As principais bibliotecas utilizadas neste projeto são:

* **Flask & Flask-CORS:** Criação da API e gerenciamento de rotas.
* **Transformers (Hugging Face) & PyTorch:** Carregamento e execução do modelo de classificação local.
* **Google Generative AI:** Integração com a IA do Google (Gemini) para geração de texto.
* **NLTK:** Biblioteca de processamento de linguagem natural (disponível no módulo auxiliar).
* **Python-Dotenv:** Gerenciamento seguro de variáveis de ambiente.

## ⚙️ Instalação e Execução

### Pré-requisitos
* Python 3.10 ou superior.
* Uma chave de API do Google Gemini (Gratuita).

### Passo a Passo

1.  **Clone o repositório e acesse a pasta:**
    ```bash
    cd desafio-back
    ```

2.  **Crie e ative o ambiente virtual:**
    * Linux/Mac:
        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```
    * Windows:
        ```bash
        python -m venv venv
        .\venv\Scripts\activate
        ```

3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure as Variáveis de Ambiente:**
    Crie um arquivo `.env` na raiz do projeto e adicione sua chave:
    ```env
    GEMINI_API_KEY=Sua_Chave_Aqui_AIza...
    ```

5.  **Execute a API:**
    ```bash
    python app.py
    ```
    O servidor iniciará em `http://localhost:5000`.

## 📡 Endpoints da API

### 1. Health Check
Verifica se o servidor está online.
* **GET** `/api/health`

### 2. Classificar Email
Apenas classifica o email sem gerar resposta.
* **POST** `/api/classify`
* **Body:**
    ```json
    { "email_content": "Texto do email aqui..." }
    ```

### 3. Analisar Completo (Classificação + Resposta)
Classifica e sugere uma resposta apropriada.
* **POST** `/api/analyze`
* **Body:**
    ```json
    { "email_content": "Gostaria de saber o status do meu pedido #1234." }
    ```