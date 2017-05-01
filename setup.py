# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
from sys import argv, version_info
import hydratk.lib.install.task as task

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
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: Implementation",
    "Programming Language :: Python :: Implementation :: CPython", 
    "Programming Language :: Python :: Implementation :: PyPy",
    "Topic :: Software Development :: Libraries :: Application Frameworks",
    "Topic :: Utilities"
]
   
def version_update(cfg, *args):
       
    if (version_info[0] == 3):
        cfg['modules'][-1] = {'module': 'git+https://github.com/webpy/webpy.git@py3#egg=webpy'}       
   
config = {
  'pre_tasks' : [
                 version_update,
                 task.install_modules
                ],

  'post_tasks' : [
                  task.set_config,
                  task.copy_files,
                  task.set_access_rights,
                  task.set_manpage
                 ],
          
  'modules' : [    
               {'module': 'hydratk',             'version': '>=0.4.0'},
               {'module': 'hydratk-ext-yoda',    'version': '>=0.2.2'},
               {'module': 'hydratk-lib-network', 'version': '>=0.2.0'},
               {'module': 'web.py',              'version': '>=0.37'}                                               
              ],
          
  'files' : {
             'config'  : {
                          'etc/hydratk/conf.d/hydratk-ext-testenv.conf' : '/etc/hydratk/conf.d'
                         },
             'data'    : {
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
                         },
             'manpage' : 'doc/testenv.1'         
            },
          
  'rights' : {
              '/var/local/hydratk' : 'a+rwx'
             }                                       
}    

task.run_pre_install(argv, config)

entry_points = {
                'console_scripts': [
                    'testenv = hydratk.extensions.testenv.bootstrapper:run_app'                               
                ]
               }                                         
                
setup(
      name='hydratk-ext-testenv',
      version='0.2.2a.dev3',
      description='Test environment for test automation exercises',
      long_description=readme,
      author='Petr Rašek, HydraTK team',
      author_email='bowman@hydratk.org, team@hydratk.org',
      url='http://extensions.hydratk.org/testenv',
      license='BSD',
      packages=find_packages('src'),
      package_dir={'' : 'src'},
      classifiers=classifiers,
      zip_safe=False, 
      entry_points=entry_points,
      keywords='hydratk,testing,test environment,web server,database',
      requires_python='>=2.6,!=3.0.*,!=3.1.*,!=3.2.*',
      platforms='Linux'   
     )

task.run_post_install(argv, config)