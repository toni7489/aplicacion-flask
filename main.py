from flask import Flask, request, render_template, send_file
import pyshorteners
import os
import random
import string
import qrcode
from io import BytesIO
import base64
import qrcode
import io
import base64
import socket


app = Flask(__name__)

#Pagina inicio
@app.route('/')
def inicio():
    return render_template('inicio.html')

# Función para acortar URL
def shorten_url(url):
    s = pyshorteners.Shortener()
    return s.tinyurl.short(url)

# Pagina acortador url
@app.route("/acortador", methods=["GET", "POST"])
def home():
    shortened_url = None
    if request.method == "POST":
        url = request.form.get("url")
        if url:
            shortened_url = shorten_url(url)
    return render_template("acortador.html", shortened_url=shortened_url)

# Pagina generar contras
@app.route('/password', methods=['GET', 'POST'])
def password():
    contrasena = None
    if request.method == 'POST':
        try:
            # Obtener el tamaño de la contraseña del formulario
            longitud = int(request.form['longitud'])
            
            # Generar la contraseña con caracteres aleatorios
            caracteres = string.ascii_letters + string.digits + string.punctuation
            contrasena = "".join(random.choice(caracteres) for i in range(longitud))
        except ValueError:
            contrasena = "Por favor ingrese un número válido."
    
    return render_template('password.html', contrasena=contrasena)

# Pagina color picker
@app.route('/colorpicker')
def colorpicker():
    return render_template('colorpicker.html')

#Generador codigo QR    
@app.route('/qr', methods=['GET', 'POST'])
def index():
    qr_code = None
    if request.method == 'POST':
        url = request.form['url']
        if url:  # Verificar si la URL está presente
            try:
                # Generar el código QR
                img = qrcode.make(url)

                # Guardar la imagen en un buffer en memoria
                img_io = io.BytesIO()
                img.save(img_io, 'PNG')
                img_io.seek(0)

                # Convertir la imagen a base64 para incrustarla en el HTML
                qr_code = base64.b64encode(img_io.getvalue()).decode('utf-8')
            except Exception as e:
                # Si ocurre un error al generar el código QR
                return f"Error al generar el código QR: {e}"
        
        # Asegurarse de devolver la plantilla
        return render_template('qr.html', qr_code=qr_code)

    # Si el método es GET, solo renderizamos el formulario vacío
    return render_template('qr.html', qr_code=None)


@app.route('/download_qr')
def download_qr():
    url = request.args.get('url')

    if not url:
        return "URL no proporcionada", 400

    # Generar el código QR
    img = qrcode.make(url)
    img_io = io.BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)

    # Enviar la imagen como archivo descargable
    return send_file(img_io, as_attachment=True, download_name='codigo_qr.png', mimetype='image/png')


# Ruta principal que renderiza 'escaner.html'
@app.route('/escaner')
def escaner():
    return render_template('escaner.html')  # Aquí renderizamos 'escaner.html'

# Ruta para procesar el formulario y realizar el escaneo
@app.route('/scan', methods=['POST'])
def scan():
    host = request.form['host']
    port_range = request.form['range']  # Recibimos el rango de puertos del formulario
    
    # Parseamos el rango de puertos (Ejemplo: 1-1024)
    try:
        start_port, end_port = map(int, port_range.split('-'))
    except ValueError:
        error_message = "El formato del rango de puertos es incorrecto. Usa el formato: 1-1024."
        return render_template('resultados-escaneo.html', error=error_message)

    try:
        ip = socket.gethostbyname(host)  # Resolución de nombre de dominio a IP
        results = []
        
        # Escanear puertos dentro del rango proporcionado
        for puerto in range(start_port, end_port + 1):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)  # Timeout de 1 segundo por puerto
            result = sock.connect_ex((ip, puerto))
            if result == 0:  # Si la conexión es exitosa, el puerto está abierto
                results.append(f"Puerto abierto: {puerto}")
            sock.close()

        # Si no se encuentran puertos abiertos, agregar mensaje correspondiente
        if not results:
            results.append("No se encontraron puertos abiertos.")
        
        return render_template('resultados-escaneo.html', host=host, ip=ip, results=results)

    except socket.gaierror:
        error_message = "El nombre de dominio o la dirección IP ingresada no es válida."
        return render_template('resultados-escaneo.html', error=error_message)
    except Exception as e:
        error_message = f"Ocurrió un error: {e}"
        return render_template('resultados-escaneo.html', error=error_message)





#Pagina vulneravilidades

@app.route('/vulnerabilidades')
def vulnerabilidades():
                     return render_template('vulnerabilidades.html')






if __name__ == '__main__':
    app.run(debug=True)

#if __name__ == '__main__':
    #app.run(host='0.0.0.0', port=5000)