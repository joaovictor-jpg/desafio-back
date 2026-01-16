
from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
from classifier import EmailClassifier
from response_generator import ResponseGenerator

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

classifier = EmailClassifier()
response_generator = ResponseGenerator()


@app.route('/api/health', methods=['GET'])
def health_check():
    """Endpoint para verificar se a API está funcionando."""
    return jsonify({
        "status": "healthy",
        "message": "API esta funcionando corretamente"
    }), 200


@app.route('/api/classify', methods=['POST'])
def classify_email():
    """
    Endpoint para classificar um email.
    
    Espera receber um JSON com:
    {
        "email_content": "conteúdo do email aqui"
    }
    
    Retorna:
    {
        "category": "Produtivo" ou "Improdutivo",
        "confidence": 0.95,
        "processed_text": "texto pré-processado"
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'email_content' not in data:
            return jsonify({
                "error": "Campo 'email_content' é obrigatório"
            }), 400
        
        email_content = data['email_content']
        
        if not email_content or not isinstance(email_content, str):
            return jsonify({
                "error": "O conteúdo do email deve ser uma string não vazia"
            }), 400
        
        logger.info(f"Classificando email com {len(email_content)} caracteres")
        
        result = classifier.classify(email_content)
        
        return jsonify({
            "category": result['category'],
            "confidence": result['confidence'],
            "processed_text": result['processed_text']
        }), 200
        
    except Exception as e:
        logger.error(f"Erro ao classificar email: {str(e)}")
        return jsonify({
            "error": f"Erro ao processar email: {str(e)}"
        }), 500


@app.route('/api/analyze', methods=['POST'])
def analyze_email():
    """
    Endpoint completo para analisar um email: classificar e gerar resposta.
    
    Espera receber um JSON com:
    {
        "email_content": "conteúdo do email aqui"
    }
    
    Retorna:
    {
        "category": "Produtivo" ou "Improdutivo",
        "confidence": 0.95,
        "suggested_response": "resposta sugerida aqui",
        "processed_text": "texto pré-processado"
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'email_content' not in data:
            return jsonify({
                "error": "Campo 'email_content' é obrigatório"
            }), 400
        
        email_content = data['email_content']
        
        if not email_content or not isinstance(email_content, str):
            return jsonify({
                "error": "O conteúdo do email deve ser uma string não vazia"
            }), 400
        
        logger.info(f"Analisando email com {len(email_content)} caracteres")
        
        classification_result = classifier.classify(email_content)
        
        suggested_response = response_generator.generate_response(
            email_content,
            classification_result['category']
        )
        
        return jsonify({
            "category": classification_result['category'],
            "confidence": classification_result['confidence'],
            "suggested_response": suggested_response,
            "processed_text": classification_result['processed_text']
        }), 200
        
    except Exception as e:
        logger.error(f"Erro ao analisar email: {str(e)}")
        return jsonify({
            "error": f"Erro ao processar email: {str(e)}"
        }), 500


if __name__ == '__main__':
    logger.info("Iniciando servidor Flask...")
    app.run(host='0.0.0.0', port=5000, debug=True)
