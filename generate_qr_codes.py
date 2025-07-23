import qrcode
import uuid
import os

BOT_USERNAME = "@registration_test1_bot"
QR_DIR = "qr_codes"  # QR kodlar papkasi

os.makedirs(QR_DIR, exist_ok=True)

for i in range(10):
    unique_token = str(uuid.uuid4())[:8]
    link = f"https://t.me/{BOT_USERNAME}?start={unique_token}"

    img = qrcode.make(link)
    file_path = os.path.join(QR_DIR, f"{unique_token}.png")
    img.save(file_path)

    print(f"{i+1}) Token: {unique_token} → {link}")
