from flask import Flask
import pika
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import threading
import argparse
import datetime

app = Flask(__name__)
Base = declarative_base()

# Definir la clase del modelo de la tabla de la base de datos
class Mensaje(Base):
    __tablename__ = 'mensajes'
    id = Column(Integer, primary_key=True)
    contenido = Column(String)
    hora = Column(DateTime)  # Agregar columna para la hora de la alerta
    critico = Column(Boolean)

# Configurar la conexión a la base de datos SQLite
engine = create_engine('sqlite:///eventos.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='alertas')

@app.route('/')
def index():
    return 'Microservicio de eventos'

def recibir_alerta():
    while True:
        method_frame, header_frame, body = channel.basic_get(queue='alertas', auto_ack=True)
        if method_frame:
            mensaje = body.decode('utf-8')
            guardar_mensaje(mensaje)

def guardar_mensaje(mensaje):
    # Separar la hora del mensaje recibido
    parts = mensaje.split(': ', 2)
    hora_str = parts[0]  # Hora del mensaje
    contenido = parts[1]  # Contenido del mensaje
    critico = int(parts[2])

    # Guardar el mensaje en la base de datos
    session = Session()
    nuevo_mensaje = Mensaje(contenido=contenido, hora=datetime.datetime.strptime(hora_str, "%Y-%m-%d %H:%M:%S"), critico=critico)
    session.add(nuevo_mensaje)
    session.commit()
    session.close()

if __name__ == '__main__':
    # Crear un hilo para recibir las alertas en segundo plano
    thread = threading.Thread(target=recibir_alerta)
    thread.daemon = True  # El hilo se detendrá cuando se detenga el programa principal
    thread.start()

    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', type=int, default=5000, help='Port to run the server on')
    args = parser.parse_args()
    
    # Ejecutar la aplicación Flask en el hilo principal
    app.run(debug=True, port=args.port)
