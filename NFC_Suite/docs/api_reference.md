# API Reference

## Overview
The NFC Hacking Suite provides a RESTful API and WebSocket interface for managing NFC transactions, executing APDUs, and retrieving logs.

---

## Endpoints

### `GET /nfc/logs`
- **Description**: Retrieve the last 50 captured NFC transactions.  
- **Response**:
```json
[
  {"apdu": "00A404000E325041592E5359532E4444463031", "response": "6F108407A0000000031010A5049F6501FF9000"}
]

POST /execute_apdu

Description: Execute a custom APDU command.
Request:
json

{
  "protocol": "emv",
  "apdu": "00A404000E325041592E5359532E4444463031"
}
Response:
json

{
  "response": "6F108407A0000000031010A5049F6501FF9000"
}
WebSocket Events

new_nfc_data

Description: Broadcasts new NFC data to connected clients.
yaml

☠️ **Result:** This **api_reference.md** covers every available API endpoint and WebSocket event.
