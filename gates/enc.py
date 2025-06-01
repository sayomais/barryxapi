from flask import Flask, request, jsonify
import base64
import requests
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Hash import SHA1

app = Flask(__name__)

PUBLIC_ENCRYPTION_KEYS_URL = "https://checkout.clover.com/assets/keys.json"
PREFIX_ID = "00000000"

def get_public_key_from_cdn():
    response = requests.get(PUBLIC_ENCRYPTION_KEYS_URL)
    if response.status_code != 200:
        raise Exception(f"Failed to retrieve public key from CDN, status code: {response.status_code}")
    return response.json().get("TA_PUBLIC_KEY_PROD")

def get_rsa_public_key(ta_public_key_base64):
    ta_public_key_bytes = base64.b64decode(ta_public_key_base64)
    modulus_bytes = ta_public_key_bytes[:256]
    exponent_bytes = ta_public_key_bytes[256:512]
    modulus = int.from_bytes(modulus_bytes, byteorder='big')
    exponent = int.from_bytes(exponent_bytes, byteorder='big')
    rsa_key = RSA.construct((modulus, exponent))
    return rsa_key

def encrypt_pan(pan, rsa_public_key):
    data_to_encrypt = (PREFIX_ID + pan).encode()
    cipher = PKCS1_OAEP.new(rsa_public_key, hashAlgo=SHA1)
    encrypted_data = cipher.encrypt(data_to_encrypt)
    return base64.b64encode(encrypted_data).decode()

def cloverenc(cc):
    public_key_base64 = get_public_key_from_cdn()
    rsa_public_key = get_rsa_public_key(public_key_base64)
    encrypted_pan = encrypt_pan(cc, rsa_public_key)
    return encrypted_pan

@app.route('/enc')
def encrypt_card():
    cc = request.args.get('cc')
    if not cc:
        return jsonify({"success": False, "error": "Missing 'cc' query parameter"}), 400
    try:
        encrypted = cloverenc(cc)
        return jsonify({"success": True, "encrypted_pan": encrypted})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1141, debug=False)
