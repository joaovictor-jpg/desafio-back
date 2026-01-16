"""
Módulo para geração de respostas automáticas baseadas na classificação do email.
"""
import logging
import os
from transformers import pipeline
import torch

logger = logging.getLogger(__name__)


class ResponseGenerator:
    """Classe para gerar respostas automáticas para emails."""
    
    def __init__(self):
        """Inicializa o gerador de respostas."""
        self.device = 0 if torch.cuda.is_available() else -1
        self.generator = None
        
        try:
            logger.info("Carregando modelo para geração de respostas...")
            self.generator = pipeline(
                "text-generation",
                model="gpt2",
                device=self.device,
                max_length=150
            )
            logger.info("Modelo de geração carregado com sucesso")
        except Exception as e:
            logger.warning(f"Não foi possível carregar modelo de geração: {e}")
            logger.info("Usando templates de resposta como fallback")
    
    def _generate_with_template(self, email_content, category):
        """
        Gera resposta usando templates pré-definidos.
        
        Args:
            email_content: Conteúdo do email original
            category: Categoria do email (Produtivo ou Improdutivo)
            
        Returns:
            Resposta sugerida
        """
        email_lower = email_content.lower()
        
        if category == "Produtivo":
            if any(word in email_lower for word in ['suporte', 'ajuda', 'help', 'support']):
                return (
                    "Olá,\n\n"
                    "Obrigado por entrar em contato. Recebemos sua solicitação de suporte e "
                    "nossa equipe está analisando seu caso.\n\n"
                    "Você receberá uma resposta detalhada em breve. Caso seja urgente, "
                    "por favor entre em contato através do telefone [número do suporte].\n\n"
                    "Atenciosamente,\n"
                    "Equipe de Atendimento"
                )
            elif any(word in email_lower for word in ['status', 'atualização', 'update', 'andamento']):
                return (
                    "Olá,\n\n"
                    "Obrigado por acompanhar o status da sua solicitação. "
                    "Atualmente, está em análise pela equipe responsável.\n\n"
                    "Entraremos em contato assim que houver atualizações relevantes.\n\n"
                    "Atenciosamente,\n"
                    "Equipe de Atendimento"
                )
            elif any(word in email_lower for word in ['erro', 'bug', 'problema', 'issue', 'error']):
                return (
                    "Olá,\n\n"
                    "Obrigado por reportar o problema. Nossa equipe técnica foi notificada "
                    "e está investigando a questão.\n\n"
                    "Enviaremos uma atualização assim que identificarmos a causa e a solução.\n\n"
                    "Atenciosamente,\n"
                    "Equipe Técnica"
                )
            elif any(word in email_lower for word in ['dúvida', 'question', 'pergunta']):
                return (
                    "Olá,\n\n"
                    "Obrigado por sua dúvida. Nossa equipe está preparando uma resposta "
                    "detalhada para você.\n\n"
                    "Responderemos em breve com todas as informações necessárias.\n\n"
                    "Atenciosamente,\n"
                    "Equipe de Atendimento"
                )
            else:
                return (
                    "Olá,\n\n"
                    "Obrigado por entrar em contato. Recebemos sua mensagem e "
                    "nossa equipe está analisando sua solicitação.\n\n"
                    "Entraremos em contato em breve com mais informações.\n\n"
                    "Atenciosamente,\n"
                    "Equipe de Atendimento"
                )
        else:
            if any(word in email_lower for word in ['feliz natal', 'happy christmas', 'boas festas']):
                return (
                    "Olá,\n\n"
                    "Muito obrigado pelas felicitações! Desejamos a você e sua família "
                    "um Natal repleto de alegria e um Ano Novo cheio de realizações.\n\n"
                    "Boas festas!\n\n"
                    "Equipe"
                )
            elif any(word in email_lower for word in ['ano novo', 'new year', 'feliz ano']):
                return (
                    "Olá,\n\n"
                    "Obrigado pelas felicitações! Desejamos um próspero Ano Novo repleto "
                    "de sucesso e felicidade para você e todos os seus.\n\n"
                    "Feliz Ano Novo!\n\n"
                    "Equipe"
                )
            elif any(word in email_lower for word in ['parabéns', 'congratulations']):
                return (
                    "Olá,\n\n"
                    "Muito obrigado pelas palavras! Ficamos felizes em receber sua mensagem.\n\n"
                    "Atenciosamente,\n"
                    "Equipe"
                )
            elif any(word in email_lower for word in ['obrigado', 'agradecimento', 'thanks', 'thank you']):
                return (
                    "Olá,\n\n"
                    "Obrigado por sua mensagem! É um prazer poder ajudá-lo.\n\n"
                    "Se precisar de mais algo, não hesite em entrar em contato.\n\n"
                    "Atenciosamente,\n"
                    "Equipe"
                )
            else:
                return (
                    "Olá,\n\n"
                    "Obrigado por sua mensagem. Agradecemos o contato.\n\n"
                    "Atenciosamente,\n"
                    "Equipe"
                )
    
    def _generate_with_ai(self, email_content, category):
        """
        Gera resposta usando modelo de IA (se disponível).
        
        Args:
            email_content: Conteúdo do email original
            category: Categoria do email (Produtivo ou Improdutivo)
            
        Returns:
            Resposta sugerida
        """
        if not self.generator:
            return self._generate_with_template(email_content, category)
        
        try:
            if category == "Produtivo":
                prompt = (
                    f"Email recebido: {email_content[:200]}\n\n"
                    "Escreva uma resposta profissional e útil em português para este email de suporte/solicitação:"
                )
            else:
                prompt = (
                    f"Email recebido: {email_content[:200]}\n\n"
                    "Escreva uma resposta breve e cordial em português para este email de agradecimento/felicitação:"
                )
            
            result = self.generator(
                prompt,
                max_length=200,
                num_return_sequences=1,
                temperature=0.7,
                do_sample=True,
                pad_token_id=50256
            )
            
            generated_text = result[0]['generated_text']
            
            response = generated_text.split(prompt)[-1].strip()
            
            response = response[:500]
            response = '\n'.join([line.strip() for line in response.split('\n') if line.strip()])
            
            if len(response) > 50:
                return response
            else:
                return self._generate_with_template(email_content, category)
                
        except Exception as e:
            logger.error(f"Erro ao gerar resposta com IA: {e}")
            return self._generate_with_template(email_content, category)
    
    def generate_response(self, email_content, category):
        """
        Gera uma resposta automática baseada no email e categoria.
        
        Args:
            email_content: Conteúdo do email original
            category: Categoria do email (Produtivo ou Improdutivo)
            
        Returns:
            Resposta sugerida
        """
        try:
            return self._generate_with_template(email_content, category)
            
        except Exception as e:
            logger.error(f"Erro ao gerar resposta: {e}")
            return (
                "Olá,\n\n"
                "Obrigado por entrar em contato.\n\n"
                "Atenciosamente,\n"
                "Equipe"
            )
