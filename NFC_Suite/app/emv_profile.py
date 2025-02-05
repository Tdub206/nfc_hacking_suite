import logging
from Crypto.Hash import CMAC
from Crypto.Cipher import AES
import threading

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class EMVProfile:
    def __init__(self, pan, master_key):
        """Initializes an EMV profile with a given PAN and master key."""
        self.pan = pan
        self.master_key = master_key
        self.atc_lock = threading.Lock()  # Ensures thread-safe ATC updates
        self.atc = 1

        # Predefined APDU responses
        self.apdu_responses = {
            (0x00, 0xA4): self._select_application,
            (0x80, 0xAE): self._generate_ac
        }

    def handle_apdu(self, apdu):
        """Handles incoming APDU commands."""
        try:
            cla, ins = apdu[:2]
            handler = self.apdu_responses.get((cla, ins), self._unknown_command)
            return handler(apdu)
        except Exception as e:
            logging.error(f"Error handling APDU command: {e}")
            return bytes.fromhex("6F 00")  # General failure response

    def _select_application(self, apdu):
        """Handles SELECT (A4) APDU command."""
        return bytes.fromhex("6F 23 84 07 A0 00 00 00 03 10 10 A5 18 50 10 56 49 53 41 20 44 45 42 49 54 20 43 41 52 44 90 00")

    def _generate_ac(self, apdu):
        """Generates an ARQC (Authorization Request Cryptogram)."""
        try:
            transaction_data = apdu[5:]
            session_key = self._derive_session_key(transaction_data[:4])
            arqc = self._generate_arqc(session_key, transaction_data[4:20])

            with self.atc_lock:
                self.atc += 1  # Ensures atomic update

            return arqc + bytes.fromhex("90 00")
        except Exception as e:
            logging.error(f"Error generating ARQC: {e}")
            return bytes.fromhex("6F 00")  # General failure response

    def _derive_session_key(self, unpredictable_number):
        """Derives a session key from the master key using CMAC."""
        try:
            cmac = CMAC.new(self.master_key, ciphermod=AES)
            cmac.update(unpredictable_number + b"\x00\x00\x00\x00")
            return cmac.digest()
        except Exception as e:
            logging.error(f"Error deriving session key: {e}")
            return b"\x00" * 16  # Return a null key in case of failure

    def _generate_arqc(self, session_key, transaction_data):
        """Generates an ARQC using CMAC."""
        try:
            cmac = CMAC.new(session_key, ciphermod=AES)
            cmac.update(transaction_data)
            return cmac.digest()
        except Exception as e:
            logging.error(f"Error generating ARQC: {e}")
            return b"\x00" * 8  # Return a null cryptogram in case of failure

    def _unknown_command(self, apdu):
        """Handles unsupported APDU commands."""
        logging.warning(f"Unknown APDU command: {apdu.hex()}")
        return bytes.fromhex("6A 81")  # Command not supported
