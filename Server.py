from flask import Flask, render_template, send_file
import threading
import asyncio
import image_scanner

app = Flask(__name__)

# Ruta para servir la página de ofertas
def actualizar_ofertas():
    asyncio.run(image_scanner.obtener_ofertas())

@app.route('/')
def home():
    return send_file("index.html")

# Endpoint para actualizar ofertas manualmente
@app.route('/actualizar')
def actualizar():
    threading.Thread(target=actualizar_ofertas).start()
    return "Actualización en proceso..."

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
