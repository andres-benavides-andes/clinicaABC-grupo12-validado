import os
import firebase_admin
import random
from firebase_admin import credentials

from flask import Flask, request

app = Flask(__name__)
# Use the application default credentials
cred = credentials.ApplicationDefault()
firebase_admin.initialize_app(cred, {
'projectId': 'miso-arquitectura-325522',
})

@app.route("/")
def hello_world():
    name = os.environ.get("NAME", "World")
    return "Hello {}!".format(name)

@app.route("/validador")
def facturador():
    
    return { "Pruebas": "error de votacion"  }


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))