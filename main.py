import os
import firebase_admin
import requests
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
def validador():
    for i in range(98):
        peticiones_ok = 0
        peticiones_error = 0
        id_paiente = i + 1
        servicio_factura_1 = requests.get(f'https://facturador-1-ndwos22ynq-uc.a.run.app/facturador?id_paciente={id_paiente}')
        servicio_factura_2 = requests.get(f'https://facturador-2-ndwos22ynq-uc.a.run.app/facturador?id_paciente={id_paiente}')
        servicio_factura_3 = requests.get(f'https://facturador-3-ndwos22ynq-uc.a.run.app/facturador?id_paciente={id_paiente}')

        
        if servicio_factura_1.status_code == 200 and servicio_factura_2.status_code == 200 and servicio_factura_3.status_code == 200:
            rta_1 = servicio_factura_1.json()
            rta_2 = servicio_factura_1.json()
            rta_3 = servicio_factura_3.json()
            if rta_1["total"] == rta_2["total"]:
                if rta_1["total"] == rta_3["total"]:
                    peticiones_ok += 1
                else:
                    peticiones_error +=1
            else:
                peticiones_error +=1

    return {"peticiones correctas":peticiones_ok,"peticiones con":peticiones_error}


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))