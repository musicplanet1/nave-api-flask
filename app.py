from flask import Flask, jsonify, redirect, request
import requests
import os

app = Flask(__name__)

# 🔹 Página de prueba para saber si el servicio corre
@app.route("/")
def home():
    return "✅ Nave API Flask corriendo en Render"

# 🔹 Endpoint para testear integración
@app.route("/test/nave")
def test_nave():
    return jsonify({"status": "ok", "message": "API lista para Nave"})

# 🔹 Endpoint simulado para iniciar pago
@app.route("/payment/nave/start/<order_id>", methods=["GET"])
def start_payment(order_id):
    NAVE_TOKEN = os.getenv("NAVE_TOKEN", "REEMPLAZA_CON_TU_TOKEN")

    payload = {
        "external_id": order_id,
        "amount": 100.0,
        "currency": "ARS",
        "buyer": {
            "name": "Cliente Test",
            "email": "test@cliente.com",
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
        "Authorization": f"Token {NAVE_TOKEN}",
        "Content-Type": "application/json"
    }

    url = "https://api.ranty.io/ecommerce/payment_request/external"

    try:
        response = requests.post(url, headers=headers, json=payload)

        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                return redirect(data["data"]["checkout_url"])
            else:
                return jsonify({"error": "Falló la intención", "detail": data}), 400
        else:
            return jsonify({
                "error": "Error HTTP",
                "status": response.status_code,
                "detail": response.text
            }), response.status_code

    except Exception as e:
        return jsonify({"error": "Excepción en servidor", "detail": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
