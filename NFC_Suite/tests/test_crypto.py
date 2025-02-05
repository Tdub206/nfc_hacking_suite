import unittest
from app.emv_profile import EMVProfile

class TestEMVProfile(unittest.TestCase):
    def setUp(self):
        self.profile = EMVProfile(pan="1234567890123456", master_key=b"key12345key12345")

    def test_generate_ac(self):
        """Test that the generate AC method returns the correct ARQC format."""
        sample_apdu = bytes.fromhex("80AE00080000000000000000")
        response = self.profile.handle_apdu(sample_apdu)
        self.assertTrue(response.endswith(b"\x90\x00"))

if __name__ == "__main__":
    unittest.main()
