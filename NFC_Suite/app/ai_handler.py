import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer

class AIAPDUHandler:
    def __init__(self, model_path="gpt2-apdu"):
        self.tokenizer = GPT2Tokenizer.from_pretrained(model_path)
        self.model = GPT2LMHeadModel.from_pretrained(model_path)

    def predict_response(self, apdu_history, current_apdu):
        context = " ".join(apdu_history + [current_apdu.hex()])
        input_ids = self.tokenizer.encode(context, return_tensors="pt")
        output = self.model.generate(input_ids, max_length=input_ids.size(1) + 10, pad_token_id=self.tokenizer.eos_token_id)
        response_hex = self.tokenizer.decode(output[0], skip_special_tokens=True).split()[-1]
        return bytes.fromhex(response_hex)
