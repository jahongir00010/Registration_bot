import json
import os

TOKEN_FILE = "used_tokens.json"

def load_used_tokens():
    if not os.path.exists(TOKEN_FILE):
        return []
    with open(TOKEN_FILE, "r") as f:
        return json.load(f)

def save_used_token(token:str):
    tokens = load_used_tokens()
    tokens.append(token)
    with open(TOKEN_FILE, "w") as f:
        json.dump(tokens, f)

def is_token_used(token: str) -> bool:
    return token in load_used_tokens()
#