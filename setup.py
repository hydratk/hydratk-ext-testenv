# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
from sys import argv, version_info
from os import path, system
from subprocess import call
from pkgutil import find_loader

with open("README.rst", "r") as f:
    readme = f.read()
    
classifiers = [
    "Development Status :: 5 - Production/Stable",
    "Environment :: Console",
    "Environment :: Other Environment",
    "Intended Audience :: Developers",
    "License :: Freely Distributable",
    "Operating System :: OS Independent",   
    "License :: OSI Approved :: BSD License",
    "Programming Language :: Python",    
    "Programming Language :: Python :: 2.6",
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: 3.3",
    "Programming Language :: Python :: 3.4",
    "Programming Language :: Python :: 3.5",
    "Programming Language :: Python :: Implementation",
    "Programming Language :: Python :: Implementation :: CPython", 
    "Topic :: Software Development :: Libraries :: Application Frameworks",
    "Topic :: Utilities"
]
      
requires = [         
            'hydratk',
            'hydratk-lib-network',
            'hydratk-ext-yoda'
           ]  
           
files = {
          'etc/hydratk/conf.d/hydratk-ext-testenv.conf'              : '/etc/hydratk/conf.d',
          'var/local/hydratk/testenv/install_db.sql'                 : '/var/local/hydratk/testenv',
          'var/local/hydratk/testenv/crm.wsdl'                       : '/var/local/hydratk/testenv',
          'var/local/hydratk/testenv/crm.xsd'                        : '/var/local/hydratk/testenv',
          'tests/yodalib/hydratk/__init__.py'                        : '/var/local/hydratk/yoda/lib/yodalib/hydratk',
          'tests/yodalib/hydratk/extensions/__init__.py'             : '/var/local/hydratk/yoda/lib/yodalib/hydratk/extensions',
          'tests/yodalib/hydratk/extensions/testenv/__init__.py'     : '/var/local/hydratk/yoda/lib/yodalib/hydratk/extensions/testenv',
          'tests/yodalib/hydratk/extensions/testenv/db_int.py'       : '/var/local/hydratk/yoda/lib/yodalib/hydratk/extensions/testenv',
          'tests/yodalib/hydratk/extensions/testenv/rest_int.py'     : '/var/local/hydratk/yoda/lib/yodalib/hydratk/extensions/testenv',
          'tests/yodalib/hydratk/extensions/testenv/soap_int.py'     : '/var/local/hydratk/yoda/lib/yodalib/hydratk/extensions/testenv',
          'tests/yodahelpers/hydratk/__init__.py'                    : '/var/local/hydratk/yoda/helpers/yodahelpers/hydratk',
          'tests/yodahelpers/hydratk/extensions/__init__.py'         : '/var/local/hydratk/yoda/helpers/yodahelpers/hydratk/extensions',
          'tests/yodahelpers/hydratk/extensions/testenv/__init__.py' : '/var/local/hydratk/yoda/helpers/yodahelpers/hydratk/extensions/testenv',
          'tests/yodahelpers/hydratk/extensions/testenv/helpers.py'  : '/var/local/hydratk/yoda/helpers/yodahelpers/hydratk/extensions/testenv',
          'tests/yoda-tests/hydratk/extensions/testenv/db.jedi'      : '/var/local/hydratk/yoda/yoda-tests/hydratk/extensions/testenv',
          'tests/yoda-tests/hydratk/extensions/testenv/rest.jedi'    : '/var/local/hydratk/yoda/yoda-tests/hydratk/extensions/testenv',
          'tests/yoda-tests/hydratk/extensions/testenv/soap.jedi'    : '/var/local/hydratk/yoda/yoda-tests/hydratk/extensions/testenv' 
        }  

entry_points = {
                'console_scripts': [
                    'testenv = hydratk.extensions.testenv.bootstrapper:run_app'                               
                ]
               }                      
   
if ('install' in argv or 'bdist_egg' in argv or 'bdist_wheel' in argv):   
    if (version_info[0] == 2):    
        system('pip install web.py>=0.37')          
    elif (version_info[0] == 3 and find_loader('web') == None):
        system('pip install git+https://github.com/webpy/webpy.git@py3#egg=webpy')              
                
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