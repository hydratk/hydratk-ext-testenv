# -*- coding: utf-8 -*-
from setuptools import setup, find_packages


with open("README.rst", "r") as f:
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
            'web.py>=0.37',            
            'hydratk',
            'hydratk-lib-network',
            'hydratk-ext-yoda'
           ]  
           
data_files=[
            ('/etc/hydratk/conf.d', ['etc/hydratk/conf.d/hydratk-ext-testenv.conf']),
            ('/var/local/hydratk/testenv', ['var/local/hydratk/testenv/install_db.sql']),
            ('/var/local/hydratk/testenv', ['var/local/hydratk/testenv/crm.wsdl']),
            ('/var/local/hydratk/testenv', ['var/local/hydratk/testenv/crm.xsd']),
            ('/var/local/hydratk/yoda/lib/yodalib/testenv', ['var/local/hydratk/yoda/lib/yodalib/testenv/__init__.py']),
            ('/var/local/hydratk/yoda/lib/yodalib/testenv', ['var/local/hydratk/yoda/lib/yodalib/testenv/db_int.py']),
            ('/var/local/hydratk/yoda/lib/yodalib/testenv', ['var/local/hydratk/yoda/lib/yodalib/testenv/rest_int.py']),
            ('/var/local/hydratk/yoda/lib/yodalib/testenv', ['var/local/hydratk/yoda/lib/yodalib/testenv/soap_int.py']),
            ('/var/local/hydratk/yoda/helpers/yodahelpers/testenv', ['var/local/hydratk/yoda/helpers/yodahelpers/testenv/__init__.py']),
            ('/var/local/hydratk/yoda/helpers/yodahelpers/testenv', ['var/local/hydratk/yoda/helpers/yodahelpers/testenv/helpers.py']),
            ('/var/local/hydratk/yoda/yoda-tests/testenv', ['var/local/hydratk/yoda/yoda-tests/testenv/db.jedi']),
            ('/var/local/hydratk/yoda/yoda-tests/testenv', ['var/local/hydratk/yoda/yoda-tests/testenv/rest.jedi']),
            ('/var/local/hydratk/yoda/yoda-tests/testenv', ['var/local/hydratk/yoda/yoda-tests/testenv/soap.jedi'])   
           ]  

entry_points = {
                'console_scripts': [
                    'testenv = hydratk.extensions.testenv.bootstrapper:run_app'                               
                ]
               }                      
                
setup(name='hydratk-ext-testenv',
      version='0.2.0',
      description='Test environment for test automation exercises',
      long_description=readme,
      author='Petr Rašek',
      author_email='bowman@hydratk.org',
      url='http://extensions.hydratk.org/testenv',
      license='BSD',
      packages=find_packages('src'),
      install_requires=requires,
      package_dir={'' : 'src'},
      classifiers=classifiers,
      data_files=data_files,
      entry_points=entry_points   
     )