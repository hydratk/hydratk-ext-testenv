.. install_ext_testenv:

TestEnv
=======

You have 2 options how to install TestEnv extension.

Package
^^^^^^^

Install it via Python package managers PIP or easy_install.

  .. code-block:: bash
  
     $ sudo pip install --no-binary :all: hydratk-ext-testenv
     
  .. code-block:: bash
  
     $ sudo easy_install hydratk-ext-testenv
     
  .. note::
  
     PIP needs option --no-binary to run setup.py install.
     Otherwise it runs setup.py bdist_wheel.     

Source
^^^^^^

Download the source code from GitHub or PyPi and install it manually.
Full PyPi URL contains MD5 hash, adapt sample code.

  .. code-block:: bash
  
     $ git clone https://github.com/hydratk/hydratk-ext-testenv.git
     $ cd ./hydratk-ext-testenv
     $ sudo python setup.py install
     
  .. code-block:: bash
  
     $ wget https://python.org/pypi/hydratk-ext-testenv -O hydratk-ext-testenv.tar.gz
     $ tar -xf hydratk-ext-testenv.tar.gz
     $ cd ./hydratk-ext-testenv
     $ sudo python setup.py install
     
  .. note::
  
     Source is distributed with Sphinx (not installed automatically) documentation in directory doc. 
     Type make html to build local documentation however is it recommended to use up to date online documentation.     

Requirements
^^^^^^^^^^^^     
     
The extension requires modules web.py (automatically installed) and hydratk, hydratk-lib-network, hydratk-ext-yoda. 

  .. note::
   
     Installation for Python3 has some differences.
     Module web.py is not installed from PyPi but from https://github.com/webpy/webpy.git@py3#egg=webpy     
     
Installation
^^^^^^^^^^^^

See installation example, Python 2.7.    

  .. code-block:: bash
  
     **************************************
     *     Running pre-install tasks      *
     **************************************
     
     *** Running task: version_update ***
     
     *** Running task: install_modules ***
     Module hydratk already installed with version 0.5.0rc1
     Module hydratk-ext-yoda already installed with version 0.2.3rc1
     Module hydratk-lib-network already installed with version 0.2.1rc1
     Installing module web.py>=0.37
     pip install "web.py>=0.37"
     
     running install
     running bdist_egg
     running egg_info
     creating src/hydratk_ext_testenv.egg-info
     writing src/hydratk_ext_testenv.egg-info/PKG-INFO
     writing top-level names to src/hydratk_ext_testenv.egg-info/top_level.txt
     writing dependency_links to src/hydratk_ext_testenv.egg-info/dependency_links.txt
     writing entry points to src/hydratk_ext_testenv.egg-info/entry_points.txt
     writing manifest file 'src/hydratk_ext_testenv.egg-info/SOURCES.txt'
     reading manifest file 'src/hydratk_ext_testenv.egg-info/SOURCES.txt'
     reading manifest template 'MANIFEST.in'
     writing manifest file 'src/hydratk_ext_testenv.egg-info/SOURCES.txt'
     installing library code to build/bdist.linux-x86_64/egg
     running install_lib
     running build_py
     creating build
     creating build/lib.linux-x86_64-2.7
     creating build/lib.linux-x86_64-2.7/hydratk
     ...
     creating build/bdist.linux-x86_64/egg/EGG-INFO
     copying src/hydratk_ext_testenv.egg-info/PKG-INFO -> build/bdist.linux-x86_64/egg/EGG-INFO
     copying src/hydratk_ext_testenv.egg-info/SOURCES.txt -> build/bdist.linux-x86_64/egg/EGG-INFO
     copying src/hydratk_ext_testenv.egg-info/dependency_links.txt -> build/bdist.linux-x86_64/egg/EGG-INFO
     copying src/hydratk_ext_testenv.egg-info/entry_points.txt -> build/bdist.linux-x86_64/egg/EGG-INFO
     copying src/hydratk_ext_testenv.egg-info/not-zip-safe -> build/bdist.linux-x86_64/egg/EGG-INFO
     copying src/hydratk_ext_testenv.egg-info/top_level.txt -> build/bdist.linux-x86_64/egg/EGG-INFO
     creating dist
     creating 'dist/hydratk_ext_testenv-0.2.2rc1-py2.7.egg' and adding 'build/bdist.linux-x86_64/egg' to it
     removing 'build/bdist.linux-x86_64/egg' (and everything under it)
     Processing hydratk_ext_testenv-0.2.2rc1-py2.7.egg
     creating /usr/local/lib/python2.7/dist-packages/hydratk_ext_testenv-0.2.2rc1-py2.7.egg
     Extracting hydratk_ext_testenv-0.2.2rc1-py2.7.egg to /usr/local/lib/python2.7/dist-packages
     Adding hydratk-ext-testenv 0.2.2rc1 to easy-install.pth file
     Installing testenv script to /usr/local/bin
     Installed /usr/local/lib/python2.7/dist-packages/hydratk_ext_testenv-0.2.2rc1-py2.7.egg
     Processing dependencies for hydratk-ext-testenv==0.2.2rc1
     Finished processing dependencies for hydratk-ext-testenv==0.2.2rc1
     
     **************************************
     *     Running post-install tasks     *
     **************************************

     *** Running task: set_config ***

     Copying file etc/hydratk/conf.d/hydratk-ext-testenv.conf to /etc/hydratk/conf.d

     *** Running task: copy_files ***

     Creating directory /var/local/hydratk/testenv
     Copying file var/local/hydratk/testenv/install_db.sql to /var/local/hydratk/testenv
     Creating directory /var/local/hydratk/yoda/lib/yodalib/hydratk/extensions/testenv
     Copying file tests/yodalib/hydratk/extensions/testenv/__init__.py to /var/local/hydratk/yoda/lib/yodalib/hydratk/extensions/testenv
     Creating directory /var/local/hydratk/yoda/yoda-tests/hydratk/extensions/testenv
     Copying file tests/yoda-tests/hydratk/extensions/testenv/soap.jedi to /var/local/hydratk/yoda/yoda-tests/hydratk/extensions/testenv
     Creating directory /var/local/hydratk/yoda/helpers/yodahelpers/hydratk/extensions/testenv
     Copying file tests/yodahelpers/hydratk/extensions/testenv/helpers.py to /var/local/hydratk/yoda/helpers/yodahelpers/hydratk/extensions/testenv
     Copying file tests/yoda-tests/hydratk/extensions/testenv/rest.jedi to /var/local/hydratk/yoda/yoda-tests/hydratk/extensions/testenv
     Copying file tests/yodahelpers/hydratk/__init__.py to /var/local/hydratk/yoda/helpers/yodahelpers/hydratk
     Copying file tests/yodalib/hydratk/extensions/testenv/db_int.py to /var/local/hydratk/yoda/lib/yodalib/hydratk/extensions/testenv
     Copying file var/local/hydratk/testenv/crm.wsdl to /var/local/hydratk/testenv
     Copying file tests/yodahelpers/hydratk/extensions/testenv/__init__.py to /var/local/hydratk/yoda/helpers/yodahelpers/hydratk/extensions/testenv
     Copying file tests/yodahelpers/hydratk/extensions/__init__.py to /var/local/hydratk/yoda/helpers/yodahelpers/hydratk/extensions
     Copying file var/local/hydratk/testenv/crm.xsd to /var/local/hydratk/testenv
     Copying file tests/yodalib/hydratk/extensions/testenv/soap_int.py to /var/local/hydratk/yoda/lib/yodalib/hydratk/extensions/testenv
     Copying file tests/yoda-tests/hydratk/extensions/testenv/db.jedi to /var/local/hydratk/yoda/yoda-tests/hydratk/extensions/testenv
     Copying file tests/yodalib/hydratk/__init__.py to /var/local/hydratk/yoda/lib/yodalib/hydratk
     Copying file tests/yodalib/hydratk/extensions/testenv/rest_int.py to /var/local/hydratk/yoda/lib/yodalib/hydratk/extensions/testenv
     Copying file tests/yodalib/hydratk/extensions/__init__.py to /var/local/hydratk/yoda/lib/yodalib/hydratk/extensions

     *** Running task: set_access_rights ***

     Setting rights a+rwx for /var/local/hydratk

     *** Running task: set_manpage ***     
  

Application installs following (paths depend on your OS configuration)

* testenv command in /usr/local/bin/testenv
* modules in /usr/local/lib/python2.7/dist-packages/hydratk-ext-testenv-0.2.2-py2.7egg
* configuration file in /etc/hydratk/conf.d/hydratk-ext-testenv.conf 
* application folder in /var/local/hydratk/testenv 
* yoda scripts in /var/local/hydratk/yoda  
     
Run
^^^

When installation is finished you can run the application.

Check hydratk-ext-testenv module is installed.

  .. code-block:: bash
  
     $ pip list | grep hydratk-ext-testenv
     
     hydratk-ext-testenv (0.2.2)

Check installed extensions

  .. code-block:: bash
  
     $ htk list-extensions
     
     TestEnv: TestEnv v0.2.2 (c) [2015-2017 Petr Rašek <bowman@hydratk.org>, HydraTK team <team@hydratk.org>]
     
Type command htk help and detailed info is displayed.
Type man testenv to display manual page. 

  .. code-block:: bash
  
     $ htk help
     
     Commands:
       te-install - install testing environment database
       te-run - start testing environment
       
You can run TestEnv also in standalone mode.

  .. code-block:: bash
  
     $ testenv help        
       
     TestEnv v0.2.2 (c) 2015-2017 [Petr Rašek <bowman@hydratk.org>, HydraTK team <team@hydratk.org>]
     Usage: testenv [options] command

     Commands:
        help - prints help
        install - install testing environment database
        run - start testing environment

     Global Options:
        -c, --config <file> - reads the alternate configuration file
        -d, --debug <level> - debug turned on with specified level > 0
        -e, --debug-channel <channel number, ..> - debug channel filter turned on
        -f, --force - enforces command
        -h, --home - sets htk_root_dir to the current user home directory
        -i, --interactive - turns on interactive mode
        -l, --language <language> - sets the text output language, the list of available languages is specified in the docs
        -m, --run-mode <mode> - sets the running mode, the list of available modes is specified in the docs
                         
Upgrade
=======

Use same procedure as for installation. Use command option --upgrade for pip, easy_install, --force for setup.py.
If configuration file differs from default settings the file is backuped (extension _old) and replaced by default. Adapt the configuration if needed.

Uninstall
=========    

Run command htkuninstall. Use option -y if you want to uninstall also dependent Python modules (for advanced user).                          