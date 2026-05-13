import logging

logging.basicConfig(
    filename='logs.txt', 
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def registrar_evento(mensaje, nivel="info"):
    if nivel == "error":
        logging.error(mensaje)
    else:
        logging.info(mensaje)
