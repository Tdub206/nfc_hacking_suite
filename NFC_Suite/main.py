from app.nfc_sniffer import PassiveNFCLogger
from app.emv_profile import EMVProfile
from app.ai_handler import AIAPDUHandler
from backend.server import run_server
from app.nfc_controller import NFCReaderController
from app.apdu_manager import APDUManager
from app.telemetry import Telemetry
from app.server import start_server
import logging
import threading

# Configure Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def initialize_core_components():
    """Initializes core components of the system with error handling."""
    try:
        telemetry = Telemetry()
        platform = APDUManager(telemetry)
        ai_handler = AIAPDUHandler(model_path="gpt2-apdu")
        emv_profile = EMVProfile(pan="1234567890123456", master_key=b"key12345key12345")
        platform.register_handler("emv", emv_profile)
        logging.info("Core components initialized successfully.")
        return telemetry, platform, ai_handler
    except Exception as e:
        logging.error(f"Error initializing core components: {e}")
        return None, None, None

def start_nfc_sniffing():
    """Starts passive NFC sniffing in a separate thread."""
    try:
        nfc_logger = PassiveNFCLogger(device="usb")
        logging.info("Starting NFC sniffing...")
        nfc_logger.sniff_traffic()
    except Exception as e:
        logging.error(f"Failed to start NFC sniffing: {e}")

def start_web_server(platform, telemetry):
    """Starts the Flask + SocketIO server in a separate thread."""
    try:
        logging.info("Starting web server...")
        start_server(platform, telemetry)
    except Exception as e:
        logging.error(f"Failed to start web server: {e}")

if __name__ == "__main__":
    telemetry, platform, ai_handler = initialize_core_components()

    if not telemetry or not platform:
        logging.critical("Failed to initialize core components. Exiting.")
        exit(1)

    # Start the Web Server in a separate thread
    server_thread = threading.Thread(target=start_web_server, args=(platform, telemetry), daemon=True)
    server_thread.start()

    # Start passive NFC sniffing in a separate thread
    nfc_thread = threading.Thread(target=start_nfc_sniffing, daemon=True)
    nfc_thread.start()

    # Keep the main thread alive
    server_thread.join()
    nfc_thread.join()
