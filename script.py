# -*- coding: utf-8 -*-
"""
Created on Fri Apr 30 21:45:52 2021

@author: Besitzer
"""
# import packages
import os
import requests
import zipfile as zipfile
import rasterio
from rasterio.plot import show
import numpy as np
from matplotlib import pyplot as plt
from skimage import exposure
from osgeo import gdal

print("Welcome!")


def tiff_download(url, path, filename):
    """
    Die Funktion tiff_download erstellt unabhängig vom Betriebssystem einen Ordner "GEO_ex_folder" in dem alle
    weiteren Teile des Programmes ausgeführt werden. Außerdem wird bei jedem Schritt überprüft ob schon die
    jeweilige Datei oder Ordner schon vorhanden ist, oder ob diese bzw. dieser noch erstellt werden muss.
    Weiter lädt sie eine Zip-Datei aus einem Verzeichnis herunter und entpackt die
    in ihr enthaltene Tif Datei. Auch hier wird erst geprüft ob diese Tif Datei schon vorhanden ist.
    :return: None
    """
    # Erstelle Ordner
    # Prüft ob der Ordner bereits existiert
    if os.path.exists(path):
        # Falls der Order existiert wird das mitgeteilt
        print('Folder exists')
    else:
        # Wenn kein Ornder exitiert wird einer angelegt und mitgeteilt
        os.makedirs(path)
        print('A new folder has been created')
    
    # alle zukünftigen Operationen werden in diesem Ordner durchgeführt
    os.chdir(path)
    
    zname = os.path.join(path, url.split('/')[-1])
    
    # Es wird geprüft ob der Datensatz existiert und mitgeteilt falls er vorhanden ist
    if os.path.isfile(zname):
        print('Zip file exists')
    # Falls der Datensatz nicht vorhanden ist wird der Download gestartet
    else:
        print('Download starts')
        resp = requests.get(url)
        # abspeichern des Zip-files unter neuem Namen
        with open(zname, 'wb') as zfile:
            zfile.write(resp.content)
    # Prüfen ob ein Zip file vorhanden ist
    if os.path.isfile(filename):
        print("Tif file exists")
    # Entpacken der Zip Datei
    else:
        print('start unpacking')
        zfile = zipfile.ZipFile(zname)
        zfile.extractall()
        zfile.close()
        print('Zip unpacked')


def tifcheck(path, filename):
    """
    Diese Funktion tifcheck prüft ob das Entpacken der Zip -Datei funktioniert hat, indem in dem Ordner
    nach einer Tif Datei gesucht und gegenbenfalls der Pfad mit dem Namen der Tif Datei ausgegeben wird.
    :return: none
    """
    # für nach erstmaliger Ausführung des Programms wird nochmal überprüft ob das Enpacken funktioniert hat
    files = os.listdir(path)
    if filename in files:
        print(os.path.join(path, filename))
    else:
        print('tif does not exist, please restart the programm')


# Definierung einer Funktion zum Öffnen des Bildes
def image_read(path, filename):
    """
    Die Funktion image_read öffnet die entpackte Tif-Datei und gibt das Bild zurück
    :return: floats
    """
    image = gdal.Open(os.path.join(path, filename), gdal.GA_ReadOnly)
    image_array = image.GetRasterBand(1).ReadAsArray()
    image = None  # close the dataset
    return image_array


# Logarithmische Skalierung des Bildes
def log_scale(path, filename):
    """
    Die Funktion log_scale verlangt als Eingabeparameter das vorher geöffnete Bild, wandelt dieses in einen numpy
    array um, skaliert alle Werte größer als Null logarithmisch und weißt allen Null Werten die Bezeichnung NaN
    (not a number) zu.
    :param image: str
    :return: 2D array of floats
    """
    # lesen das Bild als numpy Array
    image_array = image_read(path, filename)
    # logarithmisch skalieren die Werte >0
    image_array[image_array != 0] = (np.log10(image_array[image_array > 0])) * 10
    # 0 Werte als nAn darstellen
    image_array[image_array == 0] = np.nan
    return image_array


# Definierung einer Funktion zur weiteren Skalierung der Daten, bzw. Kontraststreckung
def rescale_intensity(log_image):
    """
    Die Funktion rescale_intensity scaliert die das Bild anhand der Perzentile neu um einen besseren Kontrast zu
    bekommen.
    :param log_image: float
    :return:  2D array of floats
    """
    # berechnen min und max Werte im Array
    min = np.nanmin(log_image)
    max = np.nanmax(log_image)
    # Perzentile für Kontraststreckung definieren
    # und ignorieren nAn Werte
    percentiles = np.nanpercentile(log_image, (2, 98))
    # Strecken der Intensitätsstuffen, die innerhalb des 2. und 98. Perzentils liegen
    scaled = exposure.rescale_intensity(log_image,
                                        in_range=tuple(percentiles),
                                        out_range=(min, max))
    return scaled


# Definierung einer Funktion zum Screiben des neu berechneten Array als raster Bild
def image_save(array, path, filename, outname):
    """
    Die Funktion image_save kreiert zunächst eine leere Tif Datei, dann wird eine Kopie des original Rasters
    angelegt und die neu skalierte Datei in das Raster hineinkopiert. Schlussendlich das wird das
    Raster wieder gelöscht.
    :return: None
    """
    image = gdal.Open(os.path.join(path, filename), gdal.GA_ReadOnly)
    # Erstellen der neuen Datei im tiff Format
    driver = gdal.GetDriverByName('Gtiff')
    # Kopieren der Geoinformation vom input Bild in die neue raster Datei
    output_image = driver.CreateCopy(os.path.join(path, outname), image, 1)
    # Kopieren des numpy Arrays in die neue raster Datei
    output_image.GetRasterBand(1).WriteArray(array)
    # leere temporären Speicher und schließe alle Dateien
    output_image.FlushCache()
    output_image = None
    image = None


# Definierung einer Funktion zur Bildvisualisierung
def image_visualize(path, filename):
    """
    Die Funktion image_visualize visualisiert das skalierte Bild indem es erst eingelesen wird und zunächst die
    größe der Achsen festegelgt wird. Weiter wird die Legende, die Farbpallette und die Achsen definiert und
    schließlich dargestellt.
    :return: None
    """
    # Öffnen des neu berechneten Bildes mit dem Packet rasterio
    new_image = rasterio.open(os.path.join(path, filename))
    # Erstellen einer Figur und eines Subplots
    fig, ax = plt.subplots(figsize=(7, 4))
    # imshow verwenden um den Colorbar zuordnen zu können
    # das erste Band der Datei kann mit .read(1) gelesen werden
    image_hidden = ax.imshow(new_image.read(1),
                             cmap='gray')
    # Formatierung von y Achselabels um wissenschaftliche Notation zu vermeiden
    ax.get_yaxis().get_major_formatter().set_scientific(False)
    # Plotten auf der gleichen Achse mit rasterio.plot.show
    show(new_image.read(1),
         transform=new_image.transform,
         ax=ax,
         cmap='gray')
    # Colorbar unter Verwendung des jetzt ausgeblendeten Bildes hinzufügen
    cbar = fig.colorbar(image_hidden, ax=ax)
    cbar.set_label('dB')
    # Darstellung des Bildes mit Colorbar in einem Fenster
    plt.show()


if __name__ == '__main__':
    url = 'https://upload.uni-jena.de/data/60faad3254c462.96067488/GEO419_Testdatensatz.zip'
    filename = 'S1B__IW___A_20180828T171447_VV_NR_Orb_Cal_ML_TF_TC.tif'
    path = os.path.join(os.getcwd(), 'GEO_ex_folder')
    outname = 'log.tif'
    
    tiff_download(url=url, path=path, filename=filename)
    tifcheck(path=path, filename=filename)
    if not os.path.isfile(outname):
        print('log scaling')
        log_image = log_scale(path=path, filename=filename)
        print('image stretching')
        image_int = rescale_intensity(log_image)
        image_save(array=image_int, path=path, filename=filename, outname=outname)
    else:
        pass
    image_visualize(path=path, filename=outname)
