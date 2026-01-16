import os
import logging
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

class ResponseGenerator:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        
        if not api_key:
            logger.warning("⚠️ Chave GEMINI_API_KEY não encontrada no .env")
            self.model = None
        else:
            try:
                genai.configure(api_key=api_key)
                self.model = genai.GenerativeModel('gemini-flash-latest')
                logger.info("✅ Cliente Gemini configurado (Modelo: gemini-flash-latest)")
            except Exception as e:
                logger.error(f"Erro ao configurar Gemini: {e}")
                self.model = None

    def generate_response(self, email_content, category):
        if category == 'Improdutivo':
            return "Este email foi classificado como improdutivo e não requer resposta prioritária."

        if not self.model:
            return "Erro: Chave do Gemini não configurada. Verifique o arquivo .env."

        try:
            prompt = f"""
            Você é um assistente de email profissional e educado.
            Tarefa: Escreva uma resposta curta, direta e cordial para o email abaixo.
            Idioma: Português (Brasil).
            
            Email recebido:
            "{email_content}"
            
            Resposta:
            """

            response = self.model.generate_content(prompt)
            return response.text.strip()

        except Exception as e:
            error_msg = str(e)
            logger.error(f"Erro na geração com Gemini: {error_msg}")
            if "429" in error_msg or "404" in error_msg:
                return "Erro: Modelo indisponível ou limite excedido. Tente novamente mais tarde."
            
            return "Desculpe, não foi possível gerar a resposta no momento."