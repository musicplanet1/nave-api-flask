# Nave API Flask

Microservicio para integrar Nave como botón de pago externo en Odoo Online.

## 🚀 Cómo usar

1. Clonar este repo en tu PC:
   ```bash
   git clone https://github.com/TU-USUARIO/nave-api-flask.git
   cd nave-api-flask
   ```

2. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```

3. Ejecutar localmente:
   ```bash
   python app.py
   ```

4. Deploy en Render:
   - Crear nuevo Web Service en https://render.com
   - Conectar con este repo
   - Start Command:
     ```
     gunicorn app:app
     ```
   - Variables de entorno:
     - `NAVE_TOKEN = TU_TOKEN`

5. Probar:
   ```
   https://TU-SERVICIO.onrender.com/payment/nave/start/SO1234
   ```
