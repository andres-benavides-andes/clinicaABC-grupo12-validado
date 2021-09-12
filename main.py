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
    peticiones_ok = 0
    peticiones_error = 0
    fallas_ser_1 = 0
    fallas_ser_2 = 0
    fallas_ser_3 = 0
    for i in range(100):
        id_paiente = i + 1
        servicio_factura_1 = requests.get(f'https://facturador-1-ndwos22ynq-uc.a.run.app/facturador?id_paciente={id_paiente}')
        servicio_factura_2 = requests.get(f'https://facturador-2-ndwos22ynq-uc.a.run.app/facturador?id_paciente={id_paiente}')
        servicio_factura_3 = requests.get(f'https://facturador-3-ndwos22ynq-uc.a.run.app/facturador?id_paciente={id_paiente}')
        
        ser_1_ok = True
        ser_2_ok = True
        ser_3_ok = True
        message = ""
        if servicio_factura_1.status_code == 200 and servicio_factura_2.status_code == 200 and servicio_factura_3.status_code == 200:
            rta_1 = servicio_factura_1.json()
            rta_2 = servicio_factura_2.json()
            rta_3 = servicio_factura_3.json()

            if rta_1["total"] == rta_2["total"]:

                if rta_1["total"] == rta_3["total"]:
                    peticiones_ok += 1
                else:
                    ser_3_ok = False
                    peticiones_error +=1
            elif rta_2["total"] == rta_3["total"]:
                ser_1_ok = False
                peticiones_error +=1
            elif rta_1["total"] == rta_3["total"]:
                ser_2_ok = False
                peticiones_error +=1


            if ser_1_ok != True:
                fallas_ser_1 += 1
            elif ser_2_ok != True:
                fallas_ser_2 += 1
            elif ser_3_ok != True:
                fallas_ser_3 += 1
            
            

    return {"peticiones correctas":peticiones_ok,
            "peticiones inconsistentes":peticiones_error,
            "errores en microservicio facturador-1":fallas_ser_1,
            "errores en microservicio facturador-2":fallas_ser_2,
            "errores en microservicio facturador-3":fallas_ser_3,}


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))