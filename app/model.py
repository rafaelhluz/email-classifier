import os
import re
import traceback
import json
from typing import Any
from dotenv import load_dotenv

try:
    import google.generativeai as genai
except Exception as e:
    genai = None
    print(f"Erro ao importar a biblioteca Google Gemini: {e}")

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if genai is not None and GEMINI_API_KEY:
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        _gemini_client = genai.GenerativeModel('gemini-1.5-flash')
    except Exception as e:
        _gemini_client = None
        print(f"Erro ao configurar o cliente Gemini: {e}")
else:
    _gemini_client = None

async def classify_and_generate(text: str) -> dict:
    """Classifica e-mails como 'Produtivo' ou 'Improdutivo' e gera uma resposta usando a IA do Google Gemini."""
    
    classification = None
    response_text = None
    
    if _gemini_client:
        try:
            prompt = f"""Você é um assistente virtual que classifica e-mails em duas categorias: 'Produtivo' e 'Improdutivo'.
            - Categoria 'Produtivo' é para e-mails que requerem uma ação ou resposta (ex: pedido de informação, solicitação, suporte, etc.).
            - Categoria 'Improdutivo' é para e-mails que não exigem ação (ex: spam, propagandas, e-mails ofensivos, notícias, etc.).
            Sempre responda apenas com um objeto JSON, sem nenhum texto adicional antes ou depois. O formato do seu JSON deve ser:
            {{"category": "Categoria do e-mail", "response": "Sugestão de resposta"}}

            A sugestão de resposta para e-mails 'Improdutivos' deve ser sempre 'Olá! Obrigado pela mensagem. Registramos seu contato. Não há ação necessária no momento.'.
            
            Aqui está o e-mail para classificar:
            {text}"""
            
            response = await _gemini_client.generate_content_async(prompt)
            
            json_match = re.search(r"\{.*\}", response.text.strip(), re.DOTALL)
            
            if json_match:
                json_string = json_match.group(0).strip()
                data = json.loads(json_string)
                
                classification = data.get("category", "Improdutivo")
                response_text = data.get("response", "Olá! Obrigado pela mensagem. Registramos seu contato. Não há ação necessária no momento.")
            else:
                raise ValueError("A resposta da API não contém um JSON válido.")
            
        except Exception as e:
            print(f"Erro na chamada à API do Google Gemini: {e}")
            traceback.print_exc()
            classification, response_text = _heuristic_classify(text), _heuristic_response(text)
    else:
        classification, response_text = _heuristic_classify(text), _heuristic_response(text)

    return {
        "category": classification,
        "response": response_text
    }

def _heuristic_classify(text: str) -> str:
    lower_text = text.lower()
    productive_words = ["suporte", "erro", "problema", "status", "pedido", "pagamento"]
    improductive_words = ["promoção", "oferta", "propaganda", "grátis", "spam"]
    
    p = sum(lower_text.count(word) for word in productive_words)
    u = sum(lower_text.count(word) for word in improductive_words)

    if u > p:
        return "Improdutivo"
    return "Produtivo"

def _heuristic_response(text: str) -> str:
    category = _heuristic_classify(text)
    if category == "Improdutivo":
        return "Olá! Obrigado pela mensagem. Registramos seu contato. Não há ação necessária no momento."
    else:
        return "Olá! Obrigado pelo contato. Seu pedido foi registrado e está em análise. Por favor, envie o número do chamado/CPF/CNPJ ou mais detalhes para agilizar o atendimento."