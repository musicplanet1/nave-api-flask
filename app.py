from flask import Flask, request, jsonify, redirect
import requests
import os

app = Flask(__name__)

# Cargamos el token desde variables de entorno (Render -> Environment)
NAVE_TOKEN = os.getenv("NAVE_TOKEN", "DEV_TOKEN_AQUI")


@app.route("/")
def home():
    return "Nave API Flask corriendo ✅"


# Crear intención de pago
@app.route("/payment/nave/start/<order_id>", methods=["GET"])
def start_payment(order_id):
    payload = {
        "external_id": order_id,
        "amount": 1000,
        "currency": "ARS",
        "description": "Compra de prueba",
        "buyer": {
            "name": "Cliente Test",
            "email": "cliente@test.com",
            "phone": "1123456789",
            "billing_address": {
                "street_1": "Calle Falsa 123",
                "city": "Buenos Aires",
                "region": "CABA",
                "country": "AR",
                "zipcode": "1000"
            }
        }
    }

    headers = {
        # Probamos solo el token plano
        "Authorization": NAVE_TOKEN,
        "Content-Type": "application/json"
    }

    url = "https://api.ranty.io/ecommerce/payment_request/external"
    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        data = response.json()
        if data.get("success"):
            return redirect(data["data"]["checkout_url"])
        else:
            return jsonify({"error": "Fallo al crear intención", "detail": data}), 400
    else:
        return jsonify({
            "error": "Error HTTP",
            "status": response.status_code,
            "detail": response.text
        }), 500


# Callback Nave → confirma pago
@app.route("/payment/nave/callback", methods=["POST"])
def nave_callback():
    data = request.json
    # Acá deberías validar la firma/token que manda Nave en el callback
    return jsonify({"received": data}), 200


# Endpoint de debug para probar la conexión con Nave
@app.route("/test/nave", methods=["GET"])
def test_nave():
    headers = {
        "Authorization": NAVE_TOKEN,  # token plano
        "Content-Type": "application/json"
    }
    url = "https://api.ranty.io/ecommerce/payment_request/external"
    response = requests.post(url, headers=headers, json={})
    return {
        "status_code": response.status_code,
        "headers_sent": headers,
        "response_text": response.text
    }


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
