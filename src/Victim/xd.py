
import base64
import json
from Cryptodome.Cipher import AES
from Cryptodome.Protocol.KDF import scrypt
from Cryptodome.Util.Padding import unpad, pad

# Datos del archivo JSON (Ejemplo)
data_json = '''{
    "nextId": 9,
    "logins": [
        {
            "id": 1,
            "hostname": "https://etpxavier.clickedu.eu",
            "encryptedUsername": "MDoEEPgAAAAAAAAAAAAAAAAAAAEwFAYIKoZIhvcNAwcECNuGiQYPhxDdBBAHYRHxOsUe9FSFmXvi0ksW",
            "encryptedPassword": "MEIEEPgAAAAAAAAAAAAAAAAAAAEwFAYIKoZIhvcNAwcECHUuFYrj8vc0BBh8Ry++IdKEDQBCI6jvDrN8eMig7zE1syQ=",
            "guid": "{41834d4d-fb21-4737-8221-3fc935e4e71f}",
            "encType": 1
        }
    ]
}'''

# Sal y base_password proporcionados
salt = b'E\xc7\xbc\xbe,\xd1\xcf\x9d\x95\x8c\x80d3.\x93\xa3\xa9\xd9N\xff'
base_password = (b'0\x81\x810m\x06\t*\x86H\x86\xf7\r\x01\x05\r0`0A\x06\t*\x86H\x86\xf7\r\x01\x05\x0c04\x04 \xd3=\xd6\x87u\xe6~m0%_U\xd9m\xae\xf0\xcb\x1b?\x15BH\xc9\xf2\xca`"]\xedo\x1d?\x02\x01\x01\x02\x01 0\n\x06\x08*\x86H\x86\xf7\r\x02\t0\x1b\x06\t`\x86H\x01e\x03\x04\x01*\x04\x0eUt0\x1b\x06\t*\x86H\x01e\x03\x02\x1a0\x11\x06\t*\x86H\x86\xf7\r\x01\x01\x01\x01')

# Decodificación base64
def base64_decode(data):
    try:
        return base64.b64decode(data)
    except Exception as e:
        print(f"Error al decodificar Base64: {e}")
        return None

# Función de desencriptado
def decrypt_password(encrypted_password, key):
    try:
        ciphertext = base64_decode(encrypted_password)
        if ciphertext is None:
            return None
        
        # Verificar longitud del ciphertext
        if len(ciphertext) < 16:
            print("Ciphertext demasiado corto después de extraer IV")
            return None
        
        # Extraer el IV del ciphertext
        iv = ciphertext[:16]
        ciphertext = ciphertext[16:]
        
        # Verificar longitud del ciphertext después de extraer IV
        if len(ciphertext) % 16 != 0:
            print(f"Longitud del ciphertext después de extraer IV no es múltiplo de 16 bytes: {len(ciphertext)}")
            return None
        
        # Crear el cifrador AES
        cipher = AES.new(key, AES.MODE_CBC, iv)
        
        # Desencriptar y quitar el padding
        decrypted = cipher.decrypt(ciphertext)
        
        try:
            decrypted = unpad(decrypted, AES.block_size)
        except ValueError as e:
            print(f"Error en el padding: {e}")
            return None
        
        return decrypted.decode('utf-8')
    except ValueError as e:
        print(f"Error en el descifrado: {e}")
    except Exception as e:
        print(f"Error inesperado: {e}")
    return None

# Cargar el JSON
data = json.loads(data_json)

# Derivar la clave con scrypt
key = scrypt(base_password, salt, 32, N=2**14, r=8, p=1)

# Extraer y procesar cada entrada
for login in data['logins']:
    hostname = login['hostname']
    encrypted_password = login['encryptedPassword']
    
    # Intentar descifrar la contraseña
    decrypted_password = decrypt_password(encrypted_password, key)
    
    if decrypted_password:
        print(f"Contraseña para {hostname}: {decrypted_password}")
    else:
        print(f"No se pudo descifrar la contraseña para {hostname}")

