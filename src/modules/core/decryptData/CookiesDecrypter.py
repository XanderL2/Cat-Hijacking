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
        

    def __DecryptWithKey(self, data):

        encryptedData = base64.b64decode(data);
        key = self.__GetMasterKey();
        iv = encryptedData[:16];  #? Is a random value that makes an encrypted text unique 
        cipherText = encryptedData[16:]; 

        cipher = AES.new(key, AES.MODE_CBC, iv);
        decryptData = unpad(cipher.decrypt(cipherText), AES.block_size);

        return decryptData.decode("utf-8");


    def DecryptLogins(self):

        for login in self.__logins:
            print(login["id"]);
            print(login["encryptedUsername"]);
            print(login["encryptedPassword"]);
            

         








