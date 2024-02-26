import requests
import json
import random

url = 'http://127.0.0.1:5000/enviar_alerta'  # Ajusta la URL de tu API
total_mensajes = 1000

for i in range(total_mensajes):
    mensaje = f'Mensaje número {i + 1}'
    critico = random.choice([1, 0])  # Genera aleatoriamente True o False para el campo critico
    payload = {'mensaje': mensaje, 'critico': critico}  # Agrega el campo critico al payload
    headers = {'Content-Type': 'application/json'}
    try:
        response = requests.post(url, data=json.dumps(payload), headers=headers)
        response.raise_for_status()  # Lanza una excepción si la respuesta es un error HTTP
        print(f'Mensaje enviado correctamente: {mensaje}, Crítico: {bool(critico)}')
    except requests.exceptions.RequestException as e:
        print(f'Error al enviar el mensaje {mensaje}: {e}')

print('Envío masivo de mensajes completado.')