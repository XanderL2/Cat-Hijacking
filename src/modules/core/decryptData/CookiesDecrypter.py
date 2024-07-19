from modules.core.decryptData.interface.DataDecrypter import DataDecrypter
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from Crypto.Protocol.KDF import PBKDF2

import base64




class CookieesDecrypter(DataDecrypter):
    
    def __init__(self, salt, baseKey, logins):
        self.__salt = salt;
        self.__baseKey= baseKey; #?In the key4.db file is the item2 field
        self.__logins = logins;


    def __GetMasterKey(self):
        # Building the Firefox encryption and decryption key based on the base key and salt found in the key4.db file
        return PBKDF2(self.__baseKey, self.__salt, dkLen=32, count=4096); 
        

    def _DecryptWithKey(self, data):

        print(f"Data base64: {data}")
        encryptedData = base64.b64decode(data);
        key = self.__GetMasterKey();
        iv = encryptedData[:16];  #? Is a random value that makes an encrypted text unique 
        cipherText = encryptedData[16:]; 

        cipher = AES.new(key, AES.MODE_CBC, iv);

        print(f"IV en Python: {iv}");
        print(f"Data decodificada en Python {encryptedData}");


        if len(iv) != 16:
            raise ValueError("IV length is not 16 bytes")
        if len(cipherText) % 16 != 0:
            raise ValueError("CipherText length is not a multiple of 16 bytes")

        decryptData = unpad(cipher.decrypt(cipherText), AES.block_size);

        return decryptData.decode("utf-8");


    def DecryptLogins(self):

        for login in self.__logins:
            # print(f"ID: {login['id']}");
            # print(f"Username: {login['encryptedUsername']}");
            # print(f"Password: {login['encryptedPassword']}");

            print(f"ID: {login['id']}");

            print(f"Username: {self._DecryptWithKey(login['encryptedUsername'])}");
            print(f"Password: {self._DecryptWithKey(login['encryptedPassword'])}");

            

         








