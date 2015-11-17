# -*- coding: utf-8 -*-
from setuptools import setup, find_packages


with open("README.md", "r") as f:
    readme = f.readlines()
    
classifiers = [
    "Development Status :: 3 - Alpha",
    "Environment :: Console",
    "Environment :: Other Environment",
    "Intended Audience :: Developers",
    "License :: Freely Distributable",
    "Operating System :: OS Independent",   
    "License :: OSI Approved :: BSD License",
    "Programming Language :: Python",    
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.3",
    "Programming Language :: Python :: Implementation",
    "Programming Language :: Python :: Implementation :: CPython",    
    "Programming Language :: Python :: Implementation :: PyPy",    
    "Topic :: Software Development :: Libraries :: Application Frameworks",
    "Topic :: Utilities"
]

packages=[
          'hydratk.extensions.testenv' 
         ]
         
requires = [
            'hydratk',
            'web.py',
            'httplib2',
            'suds',
            'lxml',
            'jsonlib2'
           ]  
           
data_files=[
            ('/etc/hydratk/conf.d', ['etc/hydratk/conf.d/hydratk-ext-testenv.conf']),
            ('/var/local/hydratk/testenv', ['var/local/hydratk/testenv/testenv.db3']),
            ('/var/local/hydratk/yoda/helpers/testenv', ['var/local/hydratk/yoda/helpers/testenv/__init__.py']),
            ('/var/local/hydratk/yoda/helpers/testenv', ['var/local/hydratk/yoda/helpers/testenv/testenv_helpers.py']),
            ('/var/local/hydratk/yoda/yoda-tests/testenv', ['var/local/hydratk/yoda/yoda-tests/testenv/db.yoda']),
            ('/var/local/hydratk/yoda/yoda-tests/testenv', ['var/local/hydratk/yoda/yoda-tests/testenv/rest.yoda']),
            ('/var/local/hydratk/yoda/yoda-tests/testenv', ['var/local/hydratk/yoda/yoda-tests/testenv/soap.yoda'])   
           ]                    
                
setup(name='HydraTK-TestEnv',
      version='0.1.0a',
      description='Test environment for test automation exercises',
      long_description=readme,
      author='Petr Rašek',
      author_email='bowman@hydratk.org',
      url='http://extensions.hydratk.org/testenv',
      license='BSD',
      packages=find_packages('src'),
      package_dir={'' : 'src'},
      classifiers=classifiers,
      data_files=data_files 
     )