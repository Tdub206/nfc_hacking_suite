import logging
import threading
from flask import Flask, jsonify, request
from flask_socketio import SocketIO
from passive_nfc_logger import PassiveNFCLogger  # Import NFC Logger
from emv_profile import EMVProfile  # Import EMV Card Handler

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Initialize Flask & SocketIO
app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# Global NFC Logs
nfc_logs = []

# Initialize EMV Profile
emv_card = EMVProfile(pan="1234567890123456", master_key=b"key12345key12345")

# NFC Sniffer Instance
nfc_logger = PassiveNFCLogger()

def start_nfc_sniffer():
    """Runs NFC sniffing in a separate thread and sends data to clients."""
    def sniff_and_emit():
        logging.info("Starting NFC sniffer in background thread...")
        nfc_logger.sniff_traffic()

    nfc_thread = threading.Thread(target=sniff_and_emit, daemon=True)
    nfc_thread.start()

@app.route("/")
def home():
    """API Root Endpoint."""
    return jsonify({"message": "NFC Hacking Suite API Running"})

@app.route("/nfc/logs", methods=["GET"])
def get_nfc_logs():
    """Returns the last 50 NFC logs."""
    return jsonify(nfc_logs[-50:])

@app.route("/execute_apdu", methods=["POST"])
def execute_apdu():
    """Handles APDU command execution."""
    try:
        data = request.json
        apdu = bytes.fromhex(data["apdu"])

        response = emv_card.handle_apdu(apdu)

        # Log and emit NFC data
        nfc_entry = {"apdu": data["apdu"], "response": response.hex()}
        nfc_logs.append(nfc_entry)
        socketio.emit("new_nfc_data", nfc_entry)

        return jsonify({"response": response.hex()})

    except Exception as e:
        logging.error(f"Error processing APDU: {e}")
        return jsonify({"error": str(e)}), 400

@socketio.on("connect")
def handle_connect():
    """Handles WebSocket client connection."""
    logging.info("Client connected to WebSocket.")

@socketio.on("disconnect")
def handle_disconnect():
    """Handles WebSocket client disconnection."""
    logging.info("Client disconnected.")

def run_server():
    """Starts the Flask-SocketIO server."""
    start_nfc_sniffer()  # Start NFC sniffing in the background
    logging.info("Starting Flask SocketIO Server on port 5000...")
    socketio.run(app, port=5000, host="0.0.0.0")

# Run the server
if __name__ == "__main__":
    run_server()
