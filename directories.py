# -*- coding: utf-8 -*-
"""
Created on Fri Apr 30 21:45:52 2021

@author: Besitzer
"""
# import packages
import os
import requests
import zipfile36 as zipfile
import rasterio
from rasterio.plot import show
import numpy as np
from matplotlib import pyplot as plt
from skimage import exposure
from osgeo import gdal

print("Welcome!")


def script():
    """
    Diese Funktion script ist die Funktion, die alle folgenden Funktionen vereinigt. So kann das Script auch als
    eigenständige Funktion aufgerufen werden
    :return: None
    """
    def tiff_download():
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
        if os.path.exists('GEO_ex_folder'):
            # Falls der Order existiert wird das mitgeteilt
            print("Folder exists")
        else:
            # Wenn kein Ornder exitiert wird einer angelegt und mitgeteilt
            os.makedirs('GEO_ex_folder')
            print('A new folder has been created')

        # alle zukünftigen Operationen werden in diesem Ordner durchgeführt
        os.chdir('GEO_ex_folder')

        # Es wird geprüft ob der Datensatz existiert und mitgeteilt falls er vorhanden ist
        if os.path.isfile('GEO419_Testdatensatz'):
            print("Zip file File exists")
        # Falls der Datensatz nicht vorhanden ist wird der Download gestartet
        elif not os.path.isfile('GEO419_Testdatensatz'):
            print('Download starts')
            zipurl = 'https://upload.uni-jena.de/data/60faad3254c462.96067488/GEO419_Testdatensatz.zip'
            resp = requests.get(zipurl)
        # abspeichern des Zip-files unter neuem Namen
            zname = "GEO419_Testdatensatz"
            zfile = open(zname, 'wb')
            zfile.write(resp.content)
            zfile.close()
        # Prüfen ob ein Zip file vorhanden ist
        if os.path.isfile('S1B__IW___A_20180828T171447_VV_NR_Orb_Cal_ML_TF_TC.tif'):
            print("Tif file exists")
        # Entpacken der Zip Datei
        elif not os.path.isfile('S1B__IW___A_20180828T171447_VV_NR_Orb_Cal_ML_TF_TC.tif'):
            print('start unpacking')
            zfile = zipfile.ZipFile('GEO419_Testdatensatz')
            zfile.extractall()
            print('Zip unpacked')

    def tifcheck():
        """
        Diese Funktion tifcheck prüft ob das Entpacken der Zip -Datei funktioniert hat, indem in dem Ordner
        nach einer Tif Datei gesucht und gegenbenfalls der Pfad mit dem Namen der Tif Datei ausgegeben wird.
        :return: none
        """
        # für nach erstmaliger Ausführung des Programms wird nochmal überprüft ob das Entpacken funktioniert hat
        for file in os.listdir():
            if file.endswith(".tif"):
                print(os.path.join("GEO_ex_folder", file),"sucessfully unpacked")
            elif not os.path.isfile('S1B__IW___A_20180828T171447_VV_NR_Orb_Cal_ML_TF_TC.tif'):
                print('tif does not exist, please restart the programm')


    # Definierung einer Funktion zum Öffnen des Bildes
    def image_read():
        """
        Die Funktion image_read öffnet die entpackte Tif-Datei und gibt das Bild zurück
        :return: floats
        """
        image = gdal.Open("S1B__IW___A_20180828T171447_VV_NR_Orb_Cal_ML_TF_TC.tif", gdal.GA_Update)
        return image

    # Logarithmische Skalierung des Bildes
    def log_scale(image):
        """
        Die Funktion log_scale verlangt als Eingabeparameter das vorher geöffnete Bild, wandelt dieses in einen numpy
        array um, skaliert alle Werte größer als Null logarithmisch und weißt allen Null Werten die Bezeichnung NaN
        (not a number) zu.
        :param image: floats
        :return: 2D array of floats
        """
        # lesen das Bild als numpy Array
        image_array = image.GetRasterBand(1).ReadAsArray()
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
    def image_save():
        """
        Die Funktion image_save kreiert zunächst eine leere Tif Datei, dann wird eine Kopie des original Rasters
        angelegt und die neu skalierte Datei in das Raster hineinkopiert. Schlussendlich das wird das
        Raster wieder gelöscht.
        :return: None
        """
        # Erstellen der neuen Datei im tiff Format
        driver = gdal.GetDriverByName('Gtiff')
        # Kopieren der Geoinformation vom input Bild in die neue raster Datei
        output_image = driver.CreateCopy("logscaled.tif", image, 1)
        # Kopieren des numpy Arrays in die neue raster Datei
        output_image.GetRasterBand(1).WriteArray(image_int)
        #del output_image

    # Definierung einer Funktion zur Bildvisualisierung
    def image_visualize():
        """
        Die Funktion image_visualize visualisiert das skalierte Bild indem es erst eingelesen wird und zunächst die
        größe der Achsen festegelgt wird. Weiter wird die Legende, die Farbpallette und die Achsen definiert und
        schließlich dargestellt.
        :return: None
        """
        # Öffnen des neu berechneten Bildes mit dem Packet rasterio
        new_image = rasterio.open("..\GEO_ex_folder\logscaled.tif")
        # Erstellen einer Figur und eines Subplots
        fig, ax = plt.subplots(figsize=(7, 4))
        # imshow verwenden um den Colorbar zuordnen zu können
        # das erste Band der Datei kann mit .read(1) gelesen werden
        #ax.plot(range(400000, 600000, 50000), range(517500, 535000, 2500))
        #ax.ticklabel_format(useOffset=False)
        image_hidden = ax.imshow(new_image.read(1),
                                 cmap='Greys_r')
        fig.legend(title='dB', bbox_to_anchor=(0.83, 0.98), frameon=False)
        # Plotten auf der gleichen Achse mit rasterio.plot.show
        show(new_image.read(1),
                transform=new_image.transform,
                ax=ax,
                cmap='Greys_r')
        # Colorbar unter Verwendung des jetzt ausgeblendeten Bildes hinzufügen
        fig.colorbar(image_hidden, ax=ax)
        # Darstellung des Bildes mit Colorbar in einem Fenster
        plt.show()

    if __name__ == "__main__":
        tiff_download()
        tifcheck()
        image = image_read()
        log_image = log_scale(image)
        image_int = rescale_intensity(log_image)
        image_save()
        image_visualize()


if __name__ == "__main__":
    script = script()
