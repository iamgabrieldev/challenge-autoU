from flask import Flask, request, jsonify, render_template
import google.generativeai as genai
import os

app = Flask(__name__)

# Configuração da API do Gemini
GEMINI_API_KEY = "AIzaSyAjhxxKSjD2JJ5Ewim4es79XEo1qmH0who"  # Substitua pela sua chave correta
genai.configure(api_key=GEMINI_API_KEY)

# Rota principal para servir o index.html
@app.route('/')
def home():
    return render_template('index.html')

# Função para classificar o email
def classify_email(text):
    prompt = f"Classifique o seguinte email como 'Produtivo' ou 'Improdutivo':\n\n{text}\n\nCategoria:"
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt)
    return response.text.strip()

# Função para gerar resposta automática
def generate_response(category, text):
    if category.lower() == "produtivo":
        prompt = f"Gere uma resposta profissional para o seguinte email:\n\n{text}\n\nResposta:"
    else:
        prompt = f"Gere uma resposta curta e educada para o seguinte email:\n\n{text}\n\nResposta:"
    
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt)
    return response.text.strip()

# Rota para processar o email
@app.route('/process', methods=['POST'])
def process_email():
    data = request.json
    text = data['text']

    # Classificar o email
    category = classify_email(text)

    # Gerar resposta automática
    response = generate_response(category, text)

    return jsonify({
        'category': category,
        'response': response
    })

if __name__ == '__main__':
    app.run(debug=True)