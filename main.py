from flask import Flask, request, render_template
import pyshorteners
import os
import random
import string

app = Flask(__name__)

#Pagina inicio
@app.route('/')
def inicio():
    return render_template('inicio.html')

# Función para acortar URL
def shorten_url(url):
    s = pyshorteners.Shortener()
    return s.tinyurl.short(url)

# Ruta principal
@app.route("/acortador", methods=["GET", "POST"])
def home():
    shortened_url = None
    if request.method == "POST":
        url = request.form.get("url")
        if url:
            shortened_url = shorten_url(url)
    return render_template("acortador.html", shortened_url=shortened_url)

# Ruta para generar contraseña
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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
