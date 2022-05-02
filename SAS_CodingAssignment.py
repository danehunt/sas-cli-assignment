# -*- coding: utf-8 -*-
"""
Created on Sat Apr 30 15:19:32 2022

@author: Dane Hunt
"""

from cryptography.fernet import Fernet

def getInput():
    print()
    print("Commands:")
    print("E - Encrypt file")
    print("D - Decrypt file")
    print("Q - Quit")
    return input("Enter a command: ")

def loadFile():
    fileLoaded = False
    while not fileLoaded:
        filename = input("Enter the name of a file in you current working directory (ex: file.txt) or Q to quit: ")
        try:
            file = open(filename, "rb")
            message = file.read()
            file.close()
        except:
            if filename == "Q":
                return None
            print("File name " + filename + " does not exist.")
        else:
            print("Successfully loaded " + filename + "!")
            fileLoaded = True
    return message

def saveFile(message):
    filename = input("What would you like to save the new file as? (ex: file.txt): ")
    file = open(filename, "wb")
    file.write(message)
    file.close()

def encryptFile(f):
    message = loadFile()
    if message != None:
        encrypted = f.encrypt(message)
        print("File has been encrypted.")
        saveFile(encrypted)
        return encrypted

def decryptFile(f):
    message = loadFile()
    if message != None:
        try:
            decrypted = f.decrypt(message)
        except:
            print("File could not be decrypted with key.")
        else:
            print("File has been decrypted.")
            saveFile(decrypted)
            return decrypted

print("Welcome to the File Encryption CLI!")
print("-----------------------------------")
key = Fernet.generate_key()
f = Fernet(key)
user_input = ""
while user_input != "Q":
    user_input = getInput()
    if user_input == "E":
        encryptFile(f)
    elif user_input == "D":
        decryptFile(f)
    elif user_input != "Q":
        print("NOT A VAILD COMMAND, PLEASE TRY AGAIN")

