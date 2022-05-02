# -*- coding: utf-8 -*-
"""
Created on Sat Apr 30 15:19:32 2022

@author: Dane Hunt
"""

import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

# lists the possible commands and prompts the user for their command
def getInput():
    print()
    print("Commands:")
    print("E - Encrypt file")
    print("D - Decrypt file")
    print("Q - Quit")
    return input("Enter a command: ")

# loads a file and converts the contents of the file to a string
def loadFile():
    fileLoaded = False
    while not fileLoaded:
        filename = input("Enter the name of a file in you current working directory or Q to quit: ")
        try:
            file = open(filename, "rb")
            textInFile = file.read()
            file.close()
        except:
            if filename.upper() == "Q":
                return None
            print("File name " + filename + " does not exist.")
        else:
            print("Successfully loaded " + filename + "!")
            fileLoaded = True
    return textInFile

# saves text within a file of a name that is entered
def saveFile(textInFile):
    filename = input("What would you like to save the new file as?: ")
    file = open(filename, "wb")
    file.write(textInFile)
    file.close()

# encrypts a file using the current key
def encryptFile(f):
    textInFile = loadFile()
    if textInFile != None:
        encrypted = f.encrypt(textInFile)
        print("File has been encrypted.")
        saveFile(encrypted)
        return encrypted

# decrypts a file using the current key
def decryptFile(f):
    textInFile = loadFile()
    if textInFile != None:
        try:
            decrypted = f.decrypt(textInFile)
        except:
            print("File could not be decrypted with key.")
        else:
            print("File has been decrypted.")
            saveFile(decrypted)
            return decrypted

# main method
# ----------------------------------------------------------
print("Welcome to Dane's File Encryption App")
print("-------------------------------------")

# get passphrase and encode in bytes
passphrase = input("Please input your passphrase: ").encode()

# used hardcoded salt for example purposes, typically randomly generated and stored in database
# salt = os.urandom(16) in order to generate randomly
salt = b'\xdc\xe2L\xcf\x12\xceAbP\x88\xe1\xc1\xbb4\x05\x8f'

# key derivation function
# algorithm: hash algorithm used to generate key
# length: length of key in bytes
# salt: typically randomly generated and stored in database
# iterations: 390000 is current recommended # of iterations
kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=salt,
    iterations=390000,
)

# create key based on passphrase input and encode 64 bit for Fernet
key = base64.urlsafe_b64encode(kdf.derive(passphrase))

# create Fernet object using created key
f = Fernet(key)

# runs until user chooses to quit the program
user_input = ""
while user_input.upper() != "Q":
    user_input = getInput()
    if user_input.upper() == "E":
        encryptFile(f)
    elif user_input.upper() == "D":
        decryptFile(f)
    elif user_input.upper() != "Q":
        print("NOT A VAILD COMMAND, PLEASE TRY AGAIN")

