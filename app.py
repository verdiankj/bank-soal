from flask import Flask, request, jsonify
import json
import difflib

app = Flask(__name__)

# Load soal dan jawaban dari file JSON
with open('bank_soal.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Fungsi pencocokan soal berdasarkan kemiripan
def cari_jawaban(soal_masuk):
    semua_soal = [v['soal'] for v in data.values()]
    cocok = difflib.get_close_matches(soal_masuk.strip(), semua_soal, n=1, cutoff=0.6)
    if cocok:
        for v in data.values():
            if v['soal'].strip() == cocok[0]:
                return v['jawaban']
    return "❌ Jawaban tidak ditemukan."

@app.route('/api/jawab', methods=['POST'])
def jawab():
    payload = request.get_json()
    soal = payload.get('soal')
    if not soal:
        return jsonify({"error": "Parameter 'soal' diperlukan."}), 400
    jawaban = cari_jawaban(soal)
    return jsonify({"soal": soal, "jawaban": jawaban})

@app.route('/', methods=['GET'])
def home():
    return jsonify({"status": "API Aktif", "endpoint": "/api/jawab", "method": "POST"})

if __name__ == '__main__':
    app.run(debug=True)