#!/usr/bin/env python3

jpg_sign = [0xFF, 0xD8, 0xFF, 0xE0, 0x00, 0x10, 0x4A, 0x46, 0x49, 0x46, 0x00, 0x01]
avl_signes = {'jpg':bytes(jpg_sign)}

fileName = input("Enter file path :")

for _ in avl_signes:
    if _ in fileName:
        ext = _
        sign = avl_signes[ext]
        break

def xorbytes(bytearr_1, bytearr_2):
    return bytes([a ^ b for a, b in zip(bytearr_1, bytearr_2)])

def findkey(input_file,sign):
    data = input_file.read(len(sign))
    input_file.seek(0,0)
    return xorbytes(data,sign)

with open(fileName,'rb') as encryptedFile:
    key = findkey(encryptedFile, sign)
    with open('temp' + ext,'wb') as decryptedFile:
        print('Decrypting with \n', key)
        while chunk := encryptedFile.read(len(key)):
            decryptedFile.write(xorbytes(chunk,key))
print('Done.')
