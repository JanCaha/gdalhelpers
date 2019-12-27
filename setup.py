# pylint: skip-file
from setuptools import setup, find_packages

setup(name='gdalhelpers',
      version='0.1.6',
      description='GDAL helpers, checks and tools package',
      url='https://github.com/JanCaha/gdalhelpers',
      author='Jan Caha',
      author_email='jan.caha@outlook.com',
      license='MIT',
      packages=find_packages(),
      install_requires=[
          'markdown',
          'gdal',
          'numpy',
          'angles',
          'nose'
      ],
      zip_safe=False,
      test_suite='nose.collector',
      tests_require=['nose']
      )
