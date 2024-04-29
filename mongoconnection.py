import json
import os
import serial
import requests


def enviar_datos_api(data):
    url = "http://127.0.0.1:8000/api/register"
    headers = {'Content-Type': 'application/json'}
    datos_api = {
       "id": data['id'],
        "clave": data['clave'],
        "name": "Soriana",
        "value": data['value']
    }
    response = requests.post(url, headers=headers, json=datos_api)
    if response.status_code == 200:
        print("Datos enviados correctamente a la API")
    else:
        print("Error al enviar datos a la API:", response.text)

def guardar_json(data):
    with open('datos.json', 'a') as json_file:
        json.dump(data, json_file)
        json_file.write('\n')

def vaciar_json():
    if os.path.exists('datos.json'):
        os.remove('datos.json')

puerto_serial = 'COM5'
ser = serial.Serial(puerto_serial, 115200)

datos = {}
while True:
    linea = ser.readline().decode('utf-8').strip()
    partes = linea.split('-')

    if len(partes) >= 3:
        clave = partes[0]
        id = partes[1]
        value = partes[2]

        datos['clave'] = clave
        datos['id'] = id
        datos['value'] = value
        print(datos)


        enviar_datos_api(datos)
        vaciar_json()
        datos = {}
    else:
        guardar_json(datos)