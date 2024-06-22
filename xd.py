import base64
import json
import os
import sqlite3

from Crypto.Cipher import AES
from Crypto.Protocol.KDF import pbkdf2
from Crypto.Util.Padding import unpad

# Ruta a tu perfil de Firefox, modifica 'xxxxxxxx.default-release' según tu perfil
profile_path = os.path.expanduser('~/.mozilla/firefox/xxxxxxxx.default-release')

# Archivos clave
key_db_path = os.path.join(profile_path, 'key4.db')
logins_json_path = os.path.join(profile_path, 'logins.json')

def get_key_from_db(key_db_path):
    # Función para obtener la clave derivada desde key4.db

    # Conectar a la base de datos SQLite key4.db
    with sqlite3.connect(key_db_path) as conn:
        cursor = conn.cursor()

        # Obtener global_salt y item2 de metadata
        cursor.execute("SELECT item1, item2 FROM metadata WHERE id = 'password';")
        global_salt, item2 = cursor.fetchone()

        # Derivar la clave usando PBKDF2 con item2 y global_salt
        key = pbkdf2(item2, global_salt, dkLen=32, count=4096)

    return key

def decrypt_with_key(encrypted_data, key):

    # Decodificar el dato cifrado en base64 
    encrypted_data = base64.b64decode(encrypted_data)

    # Creamos el IV (Son los primeros 16 bits)
    iv = encrypted_data[:16]

    # Esto es el texto cifrado
    ciphertext = encrypted_data[16:]



    # Crear un cifrador AES en modo CBC para luego poder desencriptar datos
    cipher = AES.new(key, AES.MODE_CBC, iv)

    # Desciframos la información
    decrypted_data = unpad(cipher.decrypt(ciphertext), AES.block_size)


    # Retornamos la data descifrada en UTF-8
    return decrypted_data.decode('utf-8')




def decrypt_logins(logins_json_path, key):
    # Función para descifrar los nombres de usuario y contraseñas desde logins.json

    with open(logins_json_path, 'r') as f:
        logins_data = json.load(f)

    for login in logins_data['logins']:
        encrypted_username = login['encryptedUsername']
        encrypted_password = login['encryptedPassword']
        username = decrypt_with_key(encrypted_username, key)
        password = decrypt_with_key(encrypted_password, key)
        print(f"Hostname: {login['hostname']}")
        print(f"Username: {username}")
        print(f"Password: {password}")
        print("=" * 40)


        
if __name__ == "__main__":
    # Obtener la clave derivada desde key4.db
    key = get_key_from_db(key_db_path)
    
    # Descifrar las contraseñas desde logins.json utilizando la clave derivada
    decrypt_logins(logins_json_path, key)
