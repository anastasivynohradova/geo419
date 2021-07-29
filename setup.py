import setuptools
import os
import sys

with open('requirements.txt', "r") as f:
    requirements = f.readlines()

directory = os.path.abspath(os.path.dirname(__file__))
if sys.version_info >= (3, 0):
    with open(os.path.join(directory, 'README.md'), encoding='utf-8') as f:
        long_description = f.read()
else:
    with open(os.path.join(directory, 'README.md')) as f:
        long_description = f.read()


setuptools.setup(
    name='script',
    version='1.0.0',
    license='GPL3',
    author='Manuel Rauch, Anastasiia Vynohradova',
    author_email='manuel.rauch@uni-jena.de, anastasiia.vynohradova@uni-jena.de',
    url="https://github.com/anastasivynohradova/geo419/",
    packages=setuptools.find_packages(),
    install_requires=[req for req in requirements if req[:2] != "# "],
    zip_safe=False,
    long_description=long_description,
    long_description_content_type='text/markdown',
    include_package_data=True
)

from sphinx.setup_command import BuildDoc
cmdclass = {'build_sphinx': BuildDoc}

name = 'Abschlussaufageb GEO 419'
version = '1.0'
release = '1.0.0'
setup(
    name=name,
    author='Manuel Rauch, Anastasiia Vynohradova<',
    version=release,
    cmdclass=cmdclass,
    # these are optional and override conf.py settings
    command_options={
        'build_sphinx': {
            'project': ('setup.py', name),
            'version': ('setup.py', version),
            'release': ('setup.py', release),
            'source_dir': ('setup.py', 'doc')}},
)
