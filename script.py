# -*- coding: utf-8 -*-
"""
Created on Fri Apr 30 21:45:52 2021

@author: Besitzer
"""
import io

import requests
import zipfile36 as zipfile
print("Welcome!")

def downpack(r):
    z = zipfile.ZipFile(io.BytesIO(r.content))
    print("Geben Sie den Pfad für den Ordner ein:")
    path = input()
    z.extractall(path)

if __name__ == "__main__":
    r = requests.get("https://upload.uni-jena.de/data/605dfe08b61aa9.92877595/GEO419_Testdatensatz.zip")
    datei = downpack(r)




