# -*- coding: utf-8 -*-

"""This code is a part of Hydra Toolkit

.. module:: hydratk.extensions.testenv.translation.cs
   :platform: Unix
   :synopsis: Czech language translation for TestEnv extension
.. moduleauthor:: Petr Rašek <bowman@hydratk.org>

"""
language = {
  'name' : 'Čeština',
  'ISO-639-1' : 'cs'
} 


msg = {    
  'te_received_cmd'         : ["Obdržen příkaz: '{0}'"],  
  'te_delete_db'            : ["Mažu databázi: '{0}'"],
  'te_create_db'            : ["Vytvářím databázi: '{0}'"],
  'te_install_db'           : ["Instaluji databázi ze skriptu: '{0}'"],
  'te_db_installed'         : ["Databáze úspěšně nainstalována"],
  'te_unknown_install'      : ["Neznámý instalační skript"],
  'te_web_unknown_file'     : ["Neznámý soubor: '{0}'"],  
  'te_db_connected'         : ["Spojení s databází bylo navázáno"],
  'te_db_disconnected'      : ["Spojení s databázi bylo ukončeno"],
  'te_db_func'              : ["Volám DB funkci: '{0}' s parametry: '{1}'"],
  'te_db_unknown_entity'    : ["Neznámá entita: '{0}' s ID: '{1}'"],
  'te_db_entity_found'      : ["Nalezena entita: '{0}' s parametry: '{1}'"],
  'te_db_entity_created'    : ["Vytvořena entita: '{0}' s ID: '{1}'"],
  'te_db_entity_changed'    : ["Změněna entita: '{0}' s ID: '{1}'"],
  'te_db_role_assigned'     : ["Přidělěna role k entitě: '{0}'"],
  'te_db_role_revoked'      : ["Odebrána rola z entity: '{0}'"],
  'te_db_srv_forbidden'     : ["Služba: '{0}' je zakázána pro entitu: '{1}'"],
  'te_db_srv_assigned'      : ["Služba: '{0}' je již přidělena"],
  'te_db_unknown_srv_param' : ["Služba: '{0}' nemá povolen parametr: '{1}'"],
  'te_db_mandatory_param'   : ["Parametr: '{0}' je povinný"],
  'te_db_param_not_assigned': ["Parametr: '{0}' není přidělen"],
  'te_rest_request'         : ["Přijat REST požadavek: '{0}' s daty: '{1}'"],  
  'te_rest_func'            : ["Volám REST funkci: '{0}' s parametry: '{1}'"],
  'te_rest_unknown_entity'  : ["Neznámá entita: '{0}' s ID: '{1}'"],
  'te_rest_entity_found'    : ["Nalezena entita: '{0}' s parametry: '{1}'"],
  'te_rest_entity_created'  : ["Vytvořena entita: '{0}' s ID: '{1}'"],
  'te_rest_entity_changed'  : ["Změněna entita: '{0}' s ID: '{1}'"],  
  'te_rest_role_assigned'   : ["Přidělěna role k entitě: '{0}'"],
  'te_rest_role_revoked'    : ["Odebrána rola z entity: '{0}'"],  
  'te_soap_request'         : ["Přijat SOAP požadavek: '{0}' s daty: '{1}'"],  
  'te_soap_func'            : ["Volám SOAP funkci: '{0}' s parametry: '{1}'"],
  'te_soap_unknown_entity'  : ["Neznámá entita: '{0}' s ID: '{1}'"],
  'te_soap_entity_found'    : ["Nalezena entita: '{0}' s parametry: '{1}'"],
  'te_soap_entity_created'  : ["Vytvořena entita: '{0}' s ID: '{1}'"],
  'te_soap_entity_changed'  : ["Změněna entita: '{0}' s ID: '{1}'"],    
  'te_soap_role_assigned'   : ["Přidělěna role k entitě: '{0}'"],
  'te_soap_role_revoked'    : ["Odebrána rola z entity: '{0}'"]  
}