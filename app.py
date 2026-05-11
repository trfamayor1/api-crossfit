from flask import Flask, jsonify, request
import pandas as pd

app = Flask(__name__)

# 🔗 Pega aquí tu link CSV publicado de Google Sheets
URL_SHEET = "https://docs.google.com/spreadsheets/d/e/2PACX-1vS3dBwwqLAfI8o9BQ5fVa6ZuFA_HTAKh0dcnO5BZNfkjZpi42saRd8lMj-Rfl2TwHx1eh6nJKw6nxhm/pub?output=csv"

# -------------------------------
# Ruta principal (prueba servidor)
# -------------------------------
@app.route("/")
def home():
    return "API funcionando 💪"

# -------------------------------
# Obtener atletas (leer Sheets)
# -------------------------------
@app.route("/datos")
def datos():
    try:
        df = pd.read_csv(URL_SHEET)
        return df.to_json(orient="records")
    except Exception as e:
        return {"error": str(e)}

# -------------------------------
# Registrar atleta desde formulario
# -------------------------------
@app.route("/registro", methods=["POST"])
def registro():
    try:
        data = request.json

        nombre = data.get("nombre")
        email = data.get("email")
        plan = data.get("plan")
        vencimiento = data.get("vencimiento")

        # Leer base actual desde Google Sheets
        df = pd.read_csv(URL_SHEET)

        # Crear nuevo registro
        nuevo = pd.DataFrame([{
            "nombre": nombre,
            "email": email,
            "plan": plan,
            "vencimiento": vencimiento
        }])

        # Unir con datos existentes (simulación DB)
        df = pd.concat([df, nuevo], ignore_index=True)

        # ⚠️ Por ahora solo simulamos guardado
        # (el guardado real a Sheets lo haremos luego)
        
        return {
            "mensaje": "Atleta registrado 💪",
            "atletas_totales_simulados": len(df)
        }

    except Exception as e:
        return {"error": str(e)}

# -------------------------------
# Ejecutar app
# -------------------------------
if __name__ == "__main__":
    app.run(debug=True)