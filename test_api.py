import gspread
from google.oauth2.service_account import Credentials

# permisos que necesita la API
scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

# autenticación
creds = Credentials.from_service_account_file(
    "credenciales.json",
    scopes=scope
)

client = gspread.authorize(creds)

# abre tu hoja (pon EXACTAMENTE el nombre)
sheet = client.open("API_BOX").sheet1

# lee una celda
print(sheet.get("A1"))