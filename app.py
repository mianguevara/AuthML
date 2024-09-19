from flask import Flask, redirect, request
import requests
import os

app = Flask(__name__)

# Variables de entorno para mantener seguras las credenciales
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")

'''CLIENT_ID = "2008472482210310"
CLIENT_SECRET = "6hnRM1H6FVwycyWO1eggyMLYrpjx65yP"
REDIRECT_URI = "https://a53d-186-81-124-162.ngrok-free.app/callback"'''

AUTH_URL = "https://auth.mercadolibre.com.co/authorization"
TOKEN_URL = "https://api.mercadolibre.com/oauth/token"

@app.route('/auth')
def auth():
    auth_redirect_url = f"{AUTH_URL}?response_type=code&client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}"
    return redirect(auth_redirect_url)

@app.route('/callback')
def callback():
    code = request.args.get('code')
    if code:
        # Intercambiar el código por un token de acceso
        token_response = requests.post(
            TOKEN_URL,
            data={
                'grant_type': 'authorization_code',
                'client_id': CLIENT_ID,
                'client_secret': CLIENT_SECRET,
                'code': code,
                'redirect_uri': REDIRECT_URI
            }
        )
        token_data = token_response.json()
        access_token = token_data.get('access_token')

        if access_token:
            # Redirigir al usuario de vuelta a la aplicación Streamlit pasando el access_token
            return redirect(f"https://infoautoapi.streamlit.app/?access_token={access_token}")
        else:
            return "Error obteniendo el token de acceso", 400
    else:
        return "Error en la autenticación", 400

if __name__ == '__main__':
    app.run(debug=True)