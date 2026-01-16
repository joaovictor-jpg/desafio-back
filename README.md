# Email Classification API - Backend Python

API Flask para classificação automática de emails e geração de respostas sugeridas usando Inteligência Artificial.

## 🎯 Funcionalidades

- **Classificação de Emails**: Classifica emails como **Produtivo** ou **Improdutivo** usando IA
- **Geração de Respostas Automáticas**: Sugere respostas adequadas baseadas na classificação
- **Pré-processamento NLP**: Remove stop words, aplica lemmatização e limpeza de texto
- **CORS Habilitado**: Pronto para integração com frontend Next.js

## 📋 Requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

## 🚀 Instalação

1. Clone o repositório ou navegue até o diretório:
```bash
cd back-end-python
```

2. Crie um ambiente virtual (recomendado):
```bash
python3 -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. As dependências do NLTK serão baixadas automaticamente na primeira execução.

## 🏃 Como Executar

Execute o servidor Flask:

```bash
python app.py
```

A API estará disponível em: `http://localhost:5000`

## 📡 Endpoints da API

### 1. Health Check
Verifica se a API está funcionando.

**GET** `/api/health`

**Resposta:**
```json
{
  "status": "healthy",
  "message": "API está funcionando corretamente"
}
```

### 2. Classificar Email
Classifica um email sem gerar resposta.

**POST** `/api/classify`

**Body:**
```json
{
  "email_content": "Preciso de ajuda com um problema no sistema. O login não está funcionando."
}
```

**Resposta:**
```json
{
  "category": "Produtivo",
  "confidence": 0.92,
  "processed_text": "preciso ajuda problema sistema login não funcionar"
}
```

### 3. Analisar Email (Classificar + Gerar Resposta)
Classifica o email e gera uma resposta sugerida.

**POST** `/api/analyze`

**Body:**
```json
{
  "email_content": "Olá, estou tendo problemas para acessar minha conta. Por favor, podem me ajudar?"
}
```

**Resposta:**
```json
{
  "category": "Produtivo",
  "confidence": 0.89,
  "suggested_response": "Olá,\n\nObrigado por entrar em contato. Recebemos sua solicitação de suporte e nossa equipe está analisando seu caso.\n\nVocê receberá uma resposta detalhada em breve...",
  "processed_text": "olá ter problema acessar conta por favor podem ajudar"
}
```

## 🔧 Estrutura do Projeto

```
back-end-python/
├── app.py                  # API Flask principal
├── nlp_processor.py        # Pré-processamento NLP
├── classifier.py           # Classificação usando IA
├── response_generator.py   # Geração de respostas automáticas
├── requirements.txt        # Dependências do projeto
└── README.md              # Este arquivo
```

## 🧠 Como Funciona

### 1. Pré-processamento NLP (`nlp_processor.py`)
- Remove URLs, emails e caracteres especiais
- Tokenização do texto
- Remoção de stop words (português e inglês)
- Lemmatização das palavras
- Limpeza e normalização

### 2. Classificação (`classifier.py`)
- Usa modelos de Transformers (Hugging Face) para análise de sentimento
- Combina análise de IA com palavras-chave específicas
- Fallback para classificação baseada em palavras-chave se o modelo não estiver disponível
- Retorna categoria (Produtivo/Improdutivo) e nível de confiança

### 3. Geração de Respostas (`response_generator.py`)
- Usa templates pré-definidos baseados no contexto do email
- Identifica palavras-chave para personalizar a resposta
- Respostas diferentes para emails produtivos (suporte, problemas, dúvidas) e improdutivos (felicitações, agradecimentos)

## 🌐 Integração com Frontend Next.js

A API já está configurada com CORS habilitado para aceitar requisições de qualquer origem. No seu frontend Next.js, você pode fazer requisições assim:

```typescript
const response = await fetch('http://localhost:5000/api/analyze', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    email_content: 'Conteúdo do email aqui'
  })
});

const data = await response.json();
console.log(data);
```

## 🎨 Categorias de Classificação

### Produtivo
Emails que requerem ação ou resposta específica:
- Solicitações de suporte técnico
- Relatórios de bugs ou erros
- Pedidos de status ou atualização
- Dúvidas sobre o sistema
- Solicitações gerais de ajuda

### Improdutivo
Emails que não necessitam ação imediata:
- Felicitações (Natal, Ano Novo, etc.)
- Agradecimentos genéricos
- Cumprimentos
- Mensagens sociais

## ⚙️ Configurações Avançadas

### Usar GPU (se disponível)
O código detecta automaticamente se há GPU disponível e usa quando possível. Para forçar CPU:

No arquivo `classifier.py` e `response_generator.py`, altere:
```python
self.device = -1  # Força uso de CPU
```

### Modelos Alternativos
Você pode usar outros modelos do Hugging Face. Altere em `classifier.py`:

```python
self.classifier = pipeline(
    "sentiment-analysis",
    model="seu-modelo-aqui",
    device=self.device
)
```

## 🐛 Troubleshooting

### Erro ao baixar modelos do NLTK
Execute manualmente no Python:
```python
import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')
```

### Modelos Hugging Face não baixam
Os modelos são baixados automaticamente na primeira execução. Certifique-se de ter conexão com internet.

### Porta 5000 já em uso
Altere a porta no final de `app.py`:
```python
app.run(host='0.0.0.0', port=5001, debug=True)
```

## 📝 Exemplos de Uso

### Teste com cURL

**Classificar email:**
```bash
curl -X POST http://localhost:5000/api/classify \
  -H "Content-Type: application/json" \
  -d '{"email_content": "Preciso de ajuda urgente com o sistema de login"}'
```

**Analisar email completo:**
```bash
curl -X POST http://localhost:5000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"email_content": "Feliz Natal e um próspero Ano Novo para toda a equipe!"}'
```

## 🔒 Segurança

Para produção, considere:
- Adicionar autenticação (JWT tokens)
- Rate limiting
- Validação mais rigorosa de entrada
- Logs de segurança
- HTTPS

## 📄 Licença

Este projeto é parte de um desafio técnico.

## 👨‍💻 Autor

Desenvolvido para automatização de classificação e resposta de emails.
