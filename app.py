from flask import Flask, request, jsonify, render_template
import google.generativeai as genai
import os

app = Flask(__name__)

GEMINI_API_KEY = "AIzaSyAjhxxKSjD2JJ5Ewim4es79XEo1qmH0who"
genai.configure(api_key=GEMINI_API_KEY)

@app.route('/')
def home():
    return render_template('index.html')

def classify_email(text):
    prompt = f"Classifique o seguinte email como 'Produtivo' ou 'Improdutivo':\n\n{text}\n\nCategoria:"
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt)
    return response.text.strip()

def generate_response(category, text):
    if category.lower() == "produtivo":
        prompt = f"Gere uma resposta profissional para o seguinte email:\n\n{text}\n\nResposta:"
    else:
        prompt = f"Gere uma resposta curta e educada para o seguinte email:\n\n{text}\n\nResposta:"
    
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt)
    return response.text.strip()

@app.route('/process', methods=['POST'])
def process_email():
    data = request.json
    text = data['text']

    category = classify_email(text)

    response = generate_response(category, text)

    return jsonify({
        'category': category,
        'response': response
    })

if __name__ == '__main__':
    app.run(debug=True)