import nfc
import logging
import threading

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class PassiveNFCLogger:
    def __init__(self, device="usb"):
        """Initializes the NFC logger."""
        self.device = device
        self.running = False
        self.nfc_thread = None

    def sniff_traffic(self):
        """Starts NFC traffic sniffing."""
        if self.running:
            logging.warning("NFC sniffer is already running.")
            return

        self.running = True
        self.nfc_thread = threading.Thread(target=self._run_sniffer, daemon=True)
        self.nfc_thread.start()
        logging.info("Passive NFC sniffing started...")

    def _run_sniffer(self):
        """Runs the NFC sniffer in a separate thread."""
        try:
            with nfc.ContactlessFrontend(self.device) as clf:
                while self.running:
                    clf.connect(rdwr={"on-connect": self._process_tag})
        except Exception as e:
            logging.error(f"Error initializing NFC reader: {e}")
            self.running = False

    def _process_tag(self, tag):
        """Processes a detected NFC tag."""
        try:
            card_uid = tag.identifier.hex()
            logging.info(f"Captured card UID: {card_uid}")
        except Exception as e:
            logging.error(f"Error processing NFC tag: {e}")

    def stop_sniffing(self):
        """Stops the NFC sniffing process."""
        self.running = False
        logging.info("Passive NFC sniffing stopped.")

# Example Usage
if __name__ == "__main__":
    nfc_logger = PassiveNFCLogger()
    try:
        nfc_logger.sniff_traffic()
        input("Press Enter to stop...\n")
    except KeyboardInterrupt:
        pass
    finally:
        nfc_logger.stop_sniffing()
