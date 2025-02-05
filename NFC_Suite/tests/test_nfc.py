import unittest
from app.nfc_sniffer import PassiveNFCLogger

class TestNFCLogger(unittest.TestCase):
    def setUp(self):
        self.logger = PassiveNFCLogger(device="test")

    def test_sniff_traffic(self):
        """Test that the logger processes tag data correctly."""
        sample_tag = type("MockTag", (object,), {"identifier": b"\x01\x02\x03\x04"})()
        self.logger._process_tag(sample_tag)
        # Check that the tag UID was processed correctly
        self.assertIn("01020304", self.logger.mqtt_client._published_messages)

if __name__ == "__main__":
    unittest.main()
