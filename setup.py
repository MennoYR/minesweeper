from setuptools import setup, find_packages

setup(name='minesweeper',
      version='0.1',
      packages=find_packages(),
      description='Minesweeper',
      author='Davey Struijk & Menno Gravemaker',
      author_email='mail@daveystruijk.com',
      license='MIT',
      install_requires=[
          'keras',
          'keras-rl',
          'h5py',
          'gym',
      ],
      zip_safe=False)
