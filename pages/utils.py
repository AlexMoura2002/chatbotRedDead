import os
import google.generativeai as genai
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Obtém a chave da API do Gemini do ambiente
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("Erro: A chave da API do Gemini não foi encontrada! Certifique-se de que o arquivo .env está configurado corretamente.")

# Configura a API do Gemini
genai.configure(api_key=API_KEY)

def gerar_resposta(pergunta):
    """
    Gera uma resposta usando o modelo Gemini 1.5 Pro sem cortar a resposta.
    """
    try:
        model = genai.GenerativeModel("gemini-1.5-pro")
        resposta = model.generate_content(pergunta, stream=True)  # Garante resposta completa

        if hasattr(resposta, 'text'):  # Verifica se há texto
            return resposta.text
        else:
            return "Desculpe, não consegui encontrar uma resposta completa."

    except Exception as e:
        return f"Erro ao gerar resposta: {str(e)}"