# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
from sys import argv
from os import path
from subprocess import call

with open("README.rst", "r") as f:
    readme = f.read()
    
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
         
requires = [
            'web.py>=0.37',            
            'hydratk',
            'hydratk-lib-network',
            'hydratk-ext-yoda'
           ]  
           
files = {
          'etc/hydratk/conf.d/hydratk-ext-testenv.conf'                    : '/etc/hydratk/conf.d',
          'var/local/hydratk/testenv/install_db.sql'                       : '/var/local/hydratk/testenv',
          'var/local/hydratk/testenv/crm.wsdl'                             : '/var/local/hydratk/testenv',
          'var/local/hydratk/testenv/crm.xsd'                              : '/var/local/hydratk/testenv',
          'var/local/hydratk/yoda/lib/yodalib/testenv/__init__.py'         : '/var/local/hydratk/yoda/lib/yodalib/testenv',
          'var/local/hydratk/yoda/lib/yodalib/testenv/db_int.py'           : '/var/local/hydratk/yoda/lib/yodalib/testenv',
          'var/local/hydratk/yoda/lib/yodalib/testenv/rest_int.py'         : '/var/local/hydratk/yoda/lib/yodalib/testenv',
          'var/local/hydratk/yoda/lib/yodalib/testenv/soap_int.py'         : '/var/local/hydratk/yoda/lib/yodalib/testenv',
          'var/local/hydratk/yoda/helpers/yodahelpers/testenv/__init__.py' : '/var/local/hydratk/yoda/helpers/yodahelpers/testenv',
          'var/local/hydratk/yoda/helpers/yodahelpers/testenv/helpers.py'  : '/var/local/hydratk/yoda/helpers/yodahelpers/testenv',
          'var/local/hydratk/yoda/yoda-tests/testenv/db.jedi'              : '/var/local/hydratk/yoda/yoda-tests/testenv',
          'var/local/hydratk/yoda/yoda-tests/testenv/rest.jedi'            : '/var/local/hydratk/yoda/yoda-tests/testenv',
          'var/local/hydratk/yoda/yoda-tests/testenv/soap.jedi'            : '/var/local/hydratk/yoda/yoda-tests/testenv' 
        }  

entry_points = {
                'console_scripts': [
                    'testenv = hydratk.extensions.testenv.bootstrapper:run_app'                               
                ]
               }                      
                
setup(
      name='hydratk-ext-testenv',
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
      zip_safe=False, 
      entry_points=entry_points   
     )

if ('install' in argv or 'bdist_egg' in argv or 'bdist_wheel' in argv):
    
    for file, dir in files.items():    
        if (not path.exists(dir)):
            call('mkdir -p {0}'.format(dir), shell=True)
            
        call('cp {0} {1}'.format(file, dir), shell=True) 
        
    call('chmod -R a+r /etc/hydratk', shell=True)
    call('chmod -R a+rwx /var/local/hydratk', shell=True)