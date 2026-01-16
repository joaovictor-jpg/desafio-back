import logging
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
import torch
from nlp_processor import NLPProcessor

logger = logging.getLogger(__name__)


class EmailClassifier:
    
    def __init__(self, model_name="distilbert-base-uncased"):
        self.nlp_processor = NLPProcessor()
        self.device = 0 if torch.cuda.is_available() else -1
        
        try:
            logger.info(f"Carregando modelo de classificação: {model_name}")
            self.classifier = pipeline(
                "sentiment-analysis",
                model="distilbert-base-uncased-finetuned-sst-2-english",
                device=self.device
            )
            logger.info("Modelo carregado com sucesso")
        except Exception as e:
            logger.warning(f"Erro ao carregar modelo padrão: {e}")
            logger.info("Usando classificação baseada em palavras-chave como fallback")
            self.classifier = None
    
    def _classify_with_model(self, processed_text):
        if not self.classifier or not processed_text:
            return self._classify_with_keywords(processed_text)
        
        try:
            if not processed_text.strip():
                processed_text = "email content"
            
            if len(processed_text) > 500:
                processed_text = processed_text[:500]
            
            result = self.classifier(processed_text)[0]
            
            label = result['label']
            score = result['score']
            
            productive_keywords = [
                'suporte', 'problema', 'erro', 'ajuda', 'solicitação',
                'status', 'atualização', 'bug', 'requisição', 'urgencia',
                'urgente', 'atendimento', 'ticket', 'caso', 'dúvida',
                'support', 'help', 'issue', 'request', 'update', 'bug',
                'urgent', 'ticket', 'case', 'question', 'problem'
            ]
            
            text_lower = processed_text.lower()
            has_productive_keywords = any(
                keyword in text_lower for keyword in productive_keywords
            )
            
            if has_productive_keywords:
                category = "Produtivo"
                confidence = min(0.95, score + 0.3)
            elif score > 0.6:
                category = "Produtivo"
                confidence = score
            else:
                category = "Improdutivo"
                confidence = 1.0 - score
            
            return category, max(0.5, min(0.99, confidence))
            
        except Exception as e:
            logger.error(f"Erro ao classificar com modelo: {e}")
            return self._classify_with_keywords(processed_text)
    
    def _classify_with_keywords(self, text):
        if not text:
            return "Improdutivo", 0.5
        
        text_lower = text.lower()
        
        productive_keywords = [
            'suporte', 'problema', 'erro', 'ajuda', 'solicitação',
            'status', 'atualização', 'bug', 'requisição', 'urgencia',
            'urgente', 'atendimento', 'ticket', 'caso', 'dúvida',
            'support', 'help', 'issue', 'request', 'update', 'bug',
            'urgent', 'ticket', 'case', 'question', 'problem',
            'necessito', 'preciso', 'favor', 'por favor', 'please'
        ]
        
        unproductive_keywords = [
            'feliz', 'natal', 'ano novo', 'parabéns', 'agradecimento',
            'obrigado', 'thanks', 'thank you', 'happy', 'congratulations',
            'cumprimento', 'saudação', 'greeting', 'salutation',
            'boas festas', 'happy holidays', 'feliz aniversário'
        ]
        
        productive_count = sum(1 for keyword in productive_keywords if keyword in text_lower)
        unproductive_count = sum(1 for keyword in unproductive_keywords if keyword in text_lower)
        
        if productive_count > unproductive_count and productive_count > 0:
            confidence = min(0.95, 0.6 + (productive_count * 0.1))
            return "Produtivo", confidence
        elif unproductive_count > productive_count and unproductive_count > 0:
            confidence = min(0.95, 0.6 + (unproductive_count * 0.1))
            return "Improdutivo", confidence
        else:
            return "Improdutivo", 0.55
    
    def classify(self, email_content):
        try:
            processed_text = self.nlp_processor.preprocess(email_content)
            
            category, confidence = self._classify_with_model(processed_text)
            
            return {
                "category": category,
                "confidence": round(confidence, 2),
                "processed_text": processed_text
            }
            
        except Exception as e:
            logger.error(f"Erro ao classificar email: {e}")
            return {
                "category": "Improdutivo",
                "confidence": 0.5,
                "processed_text": ""
            }
