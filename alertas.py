from flask import Flask, request, jsonify
import pika
import datetime

app = Flask(__name__)
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='alertas')

@app.route('/enviar_alerta', methods=['POST'])
def enviar_alerta():
    try:
        mensaje = request.json['mensaje']
        hora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Obtener la hora actual
        critico = request.json.get('critico', False)
        
        # Crear el mensaje con la hora
        mensaje = f"{hora}: {mensaje}: {critico}"

        channel.basic_publish(exchange='', routing_key='alertas', body=mensaje)
        return 'Mensaje enviado correctamente'
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
