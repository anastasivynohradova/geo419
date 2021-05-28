# -*- coding: utf-8 -*-
"""
Created on Fri Apr 30 21:45:52 2021

@author: Besitzer
"""
import io
import requests
import zipfile36 as zipfile
from osgeo import gdal
import numpy as np
from matplotlib import pyplot as plt
from PIL import Image
from cv2 import cv2
from skimage import io, exposure, data
import matplotlib.cm as cm

print("Willkommen!")

def downpack(r):
    z = zipfile.ZipFile(io.BytesIO(r.content))
    print("Geben Sie den Pfad für den Ordner ein:")
    path = input()
    z.extractall(path)

# load image as pixel array
def imageread():
     #ds = gdal.Open("S1B__IW___A_20180828T171447_VV_NR_Orb_Cal_ML_TF_TC.tif")
     image = np.array(Image.open('S1B__IW___A_20180828T171447_VV_NR_Orb_Cal_ML_TF_TC.tif'))
     #image = np.array(ds.GetRasterBand(1).ReadAsArray())
     # log skalierung
     image[image != 0] = (np.log10(image[image>0]))*10
     # 0 Werte als nAn darstellen
     image[image == 0] = np.nan
     return image

def mask(image):
    image_masked = np.ma.masked_not_equal(image, np.nan) # Use a mask to mark the NaNs
    percentiles = np.percentile(image_masked, (2, 98))
    scaled = exposure.rescale_intensity(image_masked,
                                        in_range=tuple(percentiles))
    #image_masked = cv2.normalize(image_masked, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)
    #image_masked = image_masked.astype(np.uint8)
    return scaled

def imagevisualize(image_masked):
    #fig, ax = plt.subplots()
    #ax.imshow(image, cmap=cm.gray)
    plt.imshow(image_masked, interpolation='nearest', cmap='gray')
    plt.show()
    #ax.imshow(masked_array, interpolation='nearest', cmap=cmap)



if __name__ == "__main__":
    #r = requests.get("https://upload.uni-jena.de/data/605dfe08b61aa9.92877595/GEO419_Testdatensatz.zip")
    #datei = downpack(r)
    image = imageread()
    image_masked = mask(image)
    image_combined = imagevisualize(image_masked)

    #LUT = np.zeros(256, dtype=np.uint8)
    #LUT[min:max + 1] = np.linspace(start=0, stop=255, num=(max - min) + 1, endpoint=True, dtype=np.uint8)
    #plot = Image.fromarray(LUT[cmap])
    #plt.imshow(plot, vmin = -56, vmax = 20)







