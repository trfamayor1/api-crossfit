from flask import Flask, jsonify
import pandas as pd

app = Flask(__name__)

# URL CSV público de Google Sheets
URL_SHEET = "AQUI_PONDREMOS_TU_LINK_LUEGO"

@app.route("/")
def home():
    return "API funcionando 💪"

@app.route("/datos")
def datos():
    try:
        df = pd.read_csv(URL_SHEET)
        data = df.to_dict(orient="records")
        return jsonify(data)
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)