Para probarlo
- Crear venv
- Instalar librerías necesarias
- Correr los dos microservicios:
  
  python3 eventos.py -p 5001

  python3 alertas.py -p 5000

- Correr el script para envìo masivo de mensajes:

  python3 mensajes.py
