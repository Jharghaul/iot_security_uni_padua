import socket
import logging

# Konfiguriere Logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Server-Setup
HOST = '127.0.0.1'  # Lokale Adresse (oder 0.0.0.0 für alle Schnittstellen)
PORT = 12345         # Portnummer, die der Server überwacht

def start_server():
    # Erstelle einen Socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Wiederverwendung des Ports erlauben
    
    try:
        # Binde den Server an die Adresse und Port
        server_socket.bind((HOST, PORT))
        server_socket.listen(5)  # Warteschlange für Verbindungen (max. 5 Clients)
        logger.info(f"Server started. Listening on {HOST}:{PORT}")
        
        while True:
            # Akzeptiere eine eingehende Verbindung
            client_socket, client_address = server_socket.accept()
            logger.info(f"Connection established with {client_address}")
            
            # Bearbeite die Nachrichten vom Client
            handle_client(client_socket, client_address)
    except Exception as e:
        logger.error(f"Server encountered an error: {e}")
    finally:
        server_socket.close()
        logger.info("Server shut down.")

def handle_client(client_socket, client_address):
    try:
        # Empfang der Nachricht
        data = client_socket.recv(1024).decode('utf-8')  # 1024 Bytes maximal lesen
        if data:
            logger.info(f"Received from {client_address}: {data}")
            
            # Antwort an den Client senden
            response = f"Echo: {data}"
            client_socket.sendall(response.encode('utf-8'))
    except Exception as e:
        logger.error(f"Error while handling client {client_address}: {e}")
    finally:
        # Schließe die Verbindung
        client_socket.close()
        logger.info(f"Connection with {client_address} closed.")

if __name__ == "__main__":
    start_server()
