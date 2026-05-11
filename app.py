from flask import Flask, jsonify, request
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

# ---------------- GOOGLE SHEETS LOGIN ----------------
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

creds = ServiceAccountCredentials.from_json_keyfile_name(
    "credenciales.json", scope
)

client = gspread.authorize(creds)
sheet = client.open("BASE_BOX").sheet1  # nombre de tu Google Sheet

# ---------------- TEST SERVER ----------------
@app.route("/")
def home():
    return "API funcionando 💪"

# ---------------- LEER ATLETAS ----------------
@app.route("/datos")
def datos():
    data = sheet.get_all_records()
    return jsonify(data)

# ---------------- REGISTRAR ATLETA ----------------
@app.route("/registro", methods=["POST"])
def registro():
    data = request.json

    nombre = data.get("nombre")
    email = data.get("email")
    plan = data.get("plan")
    vencimiento = data.get("vencimiento")

    sheet.append_row([nombre, email, plan, vencimiento])

    return {"mensaje": "Atleta guardado en Google Sheets 💪"}

if __name__ == "__main__":
    app.run(debug=True)