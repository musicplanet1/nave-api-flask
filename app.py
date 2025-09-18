from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return "✅ Nave API Flask corriendo en Render"

@app.route("/test")
def test():
    return jsonify({"status": "ok", "msg": "Render funciona con Flask"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
