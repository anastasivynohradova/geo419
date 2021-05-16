# -*- coding: utf-8 -*-
"""
Created on Fri Apr 30 21:45:52 2021

@author: Besitzer
"""
# import packages
import os
import requests
import zipfile36 as zipfile

#def downtiff():
#create folder
if not os.path.exists('GEO_ex_folder'):
    os.makedirs('GEO_ex_folder')

os.chdir('GEO_ex_folder')
print('A new folder has been created')


if os.path.isfile('GEO419_Testdatensatz'):
    print("Zip file File exists")
else:
    print('Download starts')
    zipurl = 'https://upload.uni-jena.de/data/605dfe08b61aa9.92877595/GEO419_Testdatensatz.zip'
    resp = requests.get(zipurl)

    zname = "GEO419_Testdatensatz"
    zfile = open(zname, 'wb')
    zfile.write(resp.content)
    zfile.close()

if os.path.isfile('GEO419_Testdatensatz'):
    print('start unpacking')
    zfile = zipfile.ZipFile('GEO419_Testdatensatz')
    zfile.extractall()
else:
    print('Zip file does not exist' )


for root, dirs, files in os.walk('GEO_ex_folder'):
    # select file name
    for file in files:
        # check the extension of files
        if file.endswith('.tif'):
            # print whole path of files
            print(os.path.join(root, file))
        else:
            print('tif does not exist, please restart the programm')


#if __name__ == "__main__":






