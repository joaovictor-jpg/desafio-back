"""
Módulo de pré-processamento de texto usando NLP.
Realiza limpeza, remoção de stop words, lemmatização, etc.
"""
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import string

try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords', quiet=True)

try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('wordnet', quiet=True)

try:
    nltk.data.find('taggers/averaged_perceptron_tagger')
except LookupError:
    nltk.download('averaged_perceptron_tagger', quiet=True)


class NLPProcessor:
    """Classe para processamento de linguagem natural."""
    
    def __init__(self):
        self.stop_words = set(stopwords.words('portuguese'))
        self.stop_words.update(set(stopwords.words('english')))
        self.lemmatizer = WordNetLemmatizer()
    
    def clean_text(self, text):
        """
        Remove caracteres especiais, URLs, emails, etc.
        
        Args:
            text: Texto a ser limpo
            
        Returns:
            Texto limpo
        """
        if not text:
            return ""
        
        text = text.lower()
        
        text = re.sub(r'http\S+|www\.\S+', '', text)
        
        text = re.sub(r'\S+@\S+', '', text)
        
        text = re.sub(r'\b\d+\b', '', text)
        
        text = re.sub(r'[^\w\s]', ' ', text)
        
        text = re.sub(r'\s+', ' ', text)
        
        text = text.strip()
        
        return text
    
    def remove_stop_words(self, tokens):
        """
        Remove stop words da lista de tokens.
        
        Args:
            tokens: Lista de tokens
            
        Returns:
            Lista de tokens sem stop words
        """
        return [token for token in tokens if token not in self.stop_words]
    
    def lemmatize(self, tokens):
        """
        Aplica lemmatização nos tokens.
        
        Args:
            tokens: Lista de tokens
            
        Returns:
            Lista de tokens lemmatizados
        """
        return [self.lemmatizer.lemmatize(token) for token in tokens]
    
    def preprocess(self, text):
        """
        Processa o texto completo: limpeza, tokenização, remoção de stop words e lemmatização.
        
        Args:
            text: Texto original
            
        Returns:
            Texto processado (como string)
        """
        if not text:
            return ""
        
        # Limpa o texto
        cleaned_text = self.clean_text(text)
        
        if not cleaned_text:
            return ""
        
        try:
            tokens = word_tokenize(cleaned_text, language='portuguese')
        except:
            tokens = word_tokenize(cleaned_text)
        
        tokens = self.remove_stop_words(tokens)
        
        tokens = self.lemmatize(tokens)
        
        tokens = [token for token in tokens if len(token) > 2]
        
        processed_text = ' '.join(tokens)
        
        return processed_text
    
    def extract_keywords(self, text, max_keywords=10):
        """
        Extrai palavras-chave do texto processado.
        
        Args:
            text: Texto original
            max_keywords: Número máximo de keywords a retornar
            
        Returns:
            Lista de palavras-chave
        """
        processed = self.preprocess(text)
        tokens = processed.split()
        
        seen = set()
        unique_tokens = []
        for token in tokens:
            if token not in seen:
                seen.add(token)
                unique_tokens.append(token)
        
        return unique_tokens[:max_keywords]
