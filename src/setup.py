from setuptools import setup, find_packages

setup(name='whale',
      version='0.1',
      description='WHALE: A management tool for Tier-2 LCG Sites',
      author='Ivano Talamo',
      author_email='ivano.talamo@gmail.com',
      url='https://github.com/talamoig/whale',
      packages=find_packages(),
      scripts=['tools/lcgwhale.py']
      )
