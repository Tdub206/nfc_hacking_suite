class APDUManager:
	def __init__(self, telemetry):
		self.telemetry = telemetry
		self.sequences = {}  # Store APDU sequences by name

	def add_sequence(self, name, sequence):
		self.sequences[name] = sequence

	def execute_sequence(self, profile_id, sequence_name, platform):
		if sequence_name not in self.sequences:
			raise ValueError(f"Sequence '{sequence_name}' not found")
		sequence = self.sequences[sequence_name]
		for apdu in sequence:
			response = platform.handle_apdu(profile_id, bytes.fromhex(apdu))
			self.telemetry.log_event("APDU_EXECUTED", {"apdu": apdu, "response": response.hex()})
