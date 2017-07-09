.. _module_ext_testenv_main:

Main
====

This sections contains module documentation of main testenv modules.

bootstrapper
^^^^^^^^^^^^

Module provides bootstrapper (method run_app) for TestEnv extension. 
You can run it in standalone mode using method command testenv (i.e. installed to /usr/local/bin/testenv).
Unit tests available at hydratk/extensions/testenv/bootstrapper/01_methods_ut.jedi

testenv
^^^^^^^

Modules provides class Extension inherited from class hydratk.core.extension.Extension.
Unit tests available at hydratk/extensions/testenv/testenv/01_methods_ut.jedi

**Methods** :

* _init_extension

Method sets extension metadata (id, name, version, author, year). 

* _check_dependencies

Method checks if all required modules are installed.

* _uninstall

Method returns additional uninstall data.

* _register_actions

Methods registers actions hooks according to profile htk (default mode) or testenv (standalone mode)

* _register_htk_actions

Method registers action hooks for default mode.

commands - te-install, te-run

* _register_standalone_actions

Method registers action hooks for standalone mode.

commands - install, help, help
long options - spec, input, output, action, element, envelope
global options - config, debug, debug-channel, language, run-mode, force, interactive, home

* install_db_fc

Method handles command te-install. It reads location of database file from configuration (/var/local/hydratk/testenv/testenv.db3).
If database is already installed the methods delete it. Database is installed using script install_db.sql (located in /var/local/hydratk/testenv).

  .. code-block:: bash
  
     htk te-install
     
     testenv install

* start_fc

Method handles command te-run. If database is not ready it installs it using method install_db_fc. Then in starts web server.

  .. code-block:: bash
  
     htk te-run
          
     testenv run
     
configuration
^^^^^^^^^^^^^

Configuration is stored in /etc/hydratk/conf.dhydratk-ext-testenv.conf   

* server_ip - IP address of web server (default 0.0.0.0)
* server_port - web server port (default 8888)
* ext_dir - directory where database is stored (including installation script, default /var/local/hydratk/testenv) 
* db_file - database filename (default testenv.db3)