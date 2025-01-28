from flask import Flask, request, jsonify
import os
from transformers import pipeline
import PyPDF2

app = Flask(__name__)

# Carregar o modelo de classificação e geração de texto
classifier = pipeline("text-classification", model="distilbert-base-uncased")
generator = pipeline("text-generation", model="gpt-2")

def extract_text_from_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

@app.route('/process', methods=['POST'])
def process_email():
    if 'file' in request.files:
        file = request.files['file']
        if file.filename.endswith('.pdf'):
            email_text = extract_text_from_pdf(file)
        elif file.filename.endswith('.txt'):
            email_text = file.read().decode('utf-8')
        else:
            return jsonify({"error": "Formato de arquivo não suportado"}), 400
    elif 'text' in request.form:
        email_text = request.form['text']
    else:
        return jsonify({"error": "Nenhum texto ou arquivo fornecido"}), 400

    # Classificar o email
    classification = classifier(email_text)[0]
    category = "Produtivo" if classification['label'] == "LABEL_1" else "Improdutivo"

    # Gerar resposta automática
    if category == "Produtivo":
        prompt = f"Responda ao seguinte email de forma profissional: {email_text}"
    else:
        prompt = f"Responda ao seguinte email de forma cordial: {email_text}"

    response = generator(prompt, max_length=50, num_return_sequences=1)[0]['generated_text']

    return jsonify({
        "category": category,
        "response": response
    })

if __name__ == '__main__':
    app.run(debug=True)