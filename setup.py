from setuptools import setup, find_packages

version = '0.0.1a'

setup(
    name='mosquito',
    packages=find_packages(), # this must be the same as the name above
    version=version,
    description="Python API to communicate with BonaDrone's Mosquito drones",
    long_description='\n\n'.join([
        open('README.rst').read(), open('CHANGES.rst').read()]),
    author='Juan Gallostra',
    author_email='juangallostra@gmail.com',
    license='GPL version 3',
    url='https://github.com/BonaDrone/mosquito-API', # use the URL to the github repo
    download_url='https://github.com/BonaDrone/mosquito-API/archive/'+version+'.tar.gz',
    keywords=['mosquito', 'API', 'MSP', 'drone', 'wrapper'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3'
    ],
    install_requires=[],
)
