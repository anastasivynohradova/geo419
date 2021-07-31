# Importieren das Packet
import setuptools
# Öffnen der Requirements Datei
with open('requirements.txt', "r") as f:
    requirements = f.readlines()

#Installieren der Packete aus dem requirements file und Metadaten des Projektes
setuptools.setup(
    name='script',
    version='1.0.0',
    #license='GPL3',
    author='Manuel Rauch, Anastasiia Vynohradova',
    author_email='manuel.rauch@uni-jena.de, anastasiia.vynohradova@uni-jena.de',
    url="https://github.com/anastasivynohradova/geo419/",
    packages=setuptools.find_packages(),
    install_requires=[req for req in requirements if req[:2] != "# "],

)