import os
from flask import Flask, render_template, request
import datetime
from pymongo import MongoClient
from dotenv import load_dotenv

def crear_app():
    app = Flask(__name__)
    cliente = MongoClient(os.getenv("MONGODB_URI"))
    app.db = cliente.blog

    #entradas = []
    entradas = [entrada for entrada in app.db.contenido.find({})]
    print(entradas)

    @app.route("/", methods = ["GET","POST"])
    def home():
        if request.method == "POST":
            titulo = request.form.get("tit")
            contenido_entrante = request.form.get("content")
            fecha_formato = datetime.datetime.today().strftime("%d-%m-%Y")
            parametros = {"titulo": titulo, "contenido":contenido_entrante, "fecha":fecha_formato}
            entradas.append(parametros)
            app.db.contenido.insert_one(parametros)

        return render_template("index.html", entradas=entradas)
    return app

if __name__ == "__main__":
    app = crear_app()
    app.run()