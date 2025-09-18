from flask import Flask, request, redirect, jsonify
import requests
import os

app = Flask(__name__)

# ⚠️ Token temporal (en producción usar client_id y secret para renovarlo)
NAVE_TOKEN = os.getenv("NAVE_TOKEN", "TU_TOKEN_AQUI")

@app.route("/")
def index():
    return "✅ Nave API Flask está corriendo"

# Crear intención de pago y redirigir al checkout Nave
@app.route("/payment/nave/start/<order_id>", methods=["GET"])
def start_payment(order_id):
    payload = {
        "platform": "odoo18_online",
        "store_id": "store_odoo",
        "callback_url": "https://mi-nave-service.onrender.com/payment/nave/callback",
        "order_id": order_id,
        "mobile": False,
        "payment_request": {
            "transactions": [
                {
                    "products": [
                        {
                            "id": "SKU123",
                            "name": "Producto Test",
                            "description": "Demo online",
                            "quantity": 1,
                            "unit_price": {"currency": "ARS", "value": "1500.00"}
                        }
                    ],
                    "amount": {"currency": "ARS", "value": "1500.00"}
                }
            ]
        },
        "buyer": {
            "user_id": "cliente@email.com",
            "doc_type": "DNI",
            "doc_number": "12345678",
            "user_email": "cliente@email.com",
            "name": "Juan Perez",
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
    print("📩 Notificación Nave:", data)
    # Aquí podrías actualizar la orden en Odoo via API
    return jsonify({"received": True}), 200

if __name__ == "__main__":
    app.run(port=5000, debug=True)
