.. install_ext_testenv:

TestEnv
=======

You have 2 options how to install TestEnv extension.

Package
^^^^^^^

Install it via Python package managers PIP or easy_install.

Filename after PIP download contains version, adapt sample code.

  .. code-block:: bash
  
     $ sudo pip download hydratk-ext-testenv
     $ sudo pip install hydratk-ext-testenv.tar.gz 
     
  .. code-block:: bash
  
     $ sudo easy_install hydratk-ext-testenv
     
  .. note::
  
     Use PIP to install package from local file for correct installation.
     When installed from remote repository, PIP sometimes doesn't call setup.py.       

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
  
     Installing module web.py>=0.37
     running install
     running bdist_egg
     running egg_info
     creating src/hydratk_ext_testenv.egg-info
     writing requirements to src/hydratk_ext_testenv.egg-info/requires.txt
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
     copying src/hydratk/__init__.py -> build/lib.linux-x86_64-2.7/hydratk
     creating build/lib.linux-x86_64-2.7/hydratk/extensions
     copying src/hydratk/extensions/__init__.py -> build/lib.linux-x86_64-2.7/hydratk/extensions
     creating build/lib.linux-x86_64-2.7/hydratk/extensions/testenv

     Installed /usr/local/lib/python2.7/dist-packages/hydratk_ext_testenv-0.2.1-py2.7.egg
     Processing dependencies for hydratk-ext-testenv==0.2.1
     Searching for hydratk-ext-yoda==0.2.2a0.dev2
     Best match: hydratk-ext-yoda 0.2.2a0.dev2
     Processing hydratk_ext_yoda-0.2.2a0.dev2-py2.7.egg
     hydratk-ext-yoda 0.2.2a0.dev2 is already the active version in easy-install.pth
     Installing yoda script to /usr/local/bin

     Using /usr/local/lib/python2.7/dist-packages/hydratk_ext_yoda-0.2.2a0.dev2-py2.7.egg
     Searching for hydratk-lib-network==0.2.0
     Best match: hydratk-lib-network 0.2.0
     Processing hydratk_lib_network-0.2.0-py2.7.egg
     hydratk-lib-network 0.2.0 is already the active version in easy-install.pth

     Using /usr/local/lib/python2.7/dist-packages/hydratk_lib_network-0.2.0-py2.7.egg
     Searching for hydratk==0.4.0
     Best match: hydratk 0.4.0
     Processing hydratk-0.4.0-py2.7.egg
     hydratk 0.4.0 is already the active version in easy-install.pth
     Installing htkprof script to /usr/local/bin
     Installing htk script to /usr/local/bin

     Using /usr/local/lib/python2.7/dist-packages/hydratk-0.4.0-py2.7.egg
     Finished processing dependencies for hydratk-ext-testenv==0.2.1

Application installs following (paths depend on your OS configuration)

* testenv command in /usr/local/bin/testenv
* modules in /usr/local/lib/python2.7/dist-packages/hydratk-ext-testenv-0.2.1-py2.7egg
* configuration file in /etc/hydratk/conf.d/hydratk-ext-testenv.conf 
* application folder in /var/local/hydratk/testenv 
* yoda scripts in /var/local/hydratk/yoda  
     
Run
^^^

When installation is finished you can run the application.

Check hydratk-ext-testenv module is installed.

  .. code-block:: bash
  
     $ pip list | grep hydratk-ext-testenv
     
     hydratk-ext-testenv (0.2.1)

Check installed extensions

  .. code-block:: bash
  
     $ htk list-extensions
     
     TestEnv: TestEnv v0.2.1 (c) [2015-2016 Petr Rašek <bowman@hydratk.org>, HydraTK team <team@hydratk.org>]
     
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
       
     TestEnv v0.2.1
     (c) 2015-2016 Petr Rašek <bowman@hydratk.org>, HydraTK team <team@hydratk.org>
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
        -i, --interactive - turns on interactive mode
        -l, --language <language> - sets the text output language, the list of available languages is specified in the docs
        -m, --run-mode <mode> - sets the running mode, the list of available modes is specified in the docs
                         
Upgrade
=======

Use same procedure as for installation. Command options --upgrade (pip, easy_install) or --force (setup.py) are not necessary.
If configuration file differs from default settings the file is backuped (extension _old) and replaced by default. Adapt the configuration if needed.

Uninstall
=========    

Run command htkuninstall testenv.                           