import setuptools

with open('requirements.txt', "r") as f:
    requirements = f.readlines()

setuptools.setup(
    name='script',
    version='1.0',
    description='Download, Entpacken, Logarithmische Skalierung und Visualisierung des logarithmisch skalierten Bilds',
    author='Manuel Rauch, Anastasiia Vynohradova',
    author_email='manuel.rauch@uni-jena.de, anastasiia.vynohradova@uni-jena.de',
    url="https://github.com/anastasivynohradova/geo419/",
    packages=setuptools.find_packages(),
    install_requires=[req for req in requirements if req[:2] != "# "],
)
