from flask import Flask, jsonify, request
from flask_cors import CORS
import gspread
from google.oauth2.service_account import Credentials
import json
import os

app = Flask(__name__)
CORS(app)

# Configuración de Google Sheets
scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

def get_sheet():
    """Conecta con Google Sheets usando variable de entorno o archivo local"""
    # Para Render: usar variable de entorno
    if os.environ.get('GOOGLE_CREDENTIALS'):
        creds_dict = json.loads(os.environ.get('GOOGLE_CREDENTIALS'))
        creds = Credentials.from_service_account_info(creds_dict, scopes=scope)
    else:
        # Para pruebas locales: usar archivo
        creds = Credentials.from_service_account_file("credenciales.json", scopes=scope)
    
    client = gspread.authorize(creds)
    # CAMBIA "API_BOX" por el nombre de tu Google Sheet
    sheet = client.open("API_BOX").sheet1
    return sheet

@app.route("/")
def home():
    return "🏋️ API Box CrossFit funcionando!"

@app.route("/datos")
def datos():
    try:
        sheet = get_sheet()
        records = sheet.get_all_records()
        return jsonify(records)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/registro", methods=["POST"])
def registro():
    try:
        data = request.json
        nombre = data.get("nombre")
        email = data.get("email")
        plan = data.get("plan")
        vencimiento = data.get("vencimiento")
        
        if not nombre or not email:
            return jsonify({"error": "Nombre y email son requeridos"}), 400
        
        sheet = get_sheet()
        sheet.append_row([nombre, email, plan, vencimiento])
        
        return jsonify({"mensaje": f"✅ Atleta {nombre} guardado en Google Sheets"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)