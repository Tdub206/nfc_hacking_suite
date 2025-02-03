from app.nfc_sniffer import PassiveNFCLogger
from app.emv_profile import EMVProfile
from app.ai_handler import AIAPDUHandler
from backend.server import run_server
from backend.telemetry import Telemetry

# Initialize telemetry system
telemetry = Telemetry()

# Initialize passive NFC sniffing
nfc_logger = PassiveNFCLogger(device="usb")

# Register EMV profile
emv_card = EMVProfile(pan="1234567890123456", master_key=b"key12345key12345")

# AI-based transaction prediction
ai_handler = AIAPDUHandler(model_path="gpt2-apdu")

# Start WebSocket API server
run_server()

# Start passive NFC sniffing
nfc_logger.sniff_traffic()
