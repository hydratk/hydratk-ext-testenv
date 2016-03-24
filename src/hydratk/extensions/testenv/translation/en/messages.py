# -*- coding: utf-8 -*-

"""This code is a part of Hydra Toolkit

.. module:: hydratk.extensions.testenv.translation.en
   :platform: Unix
   :synopsis: English language translation for TestEnv extension
.. moduleauthor:: Petr Rašek <bowman@hydratk.org>

"""

language = {
  'name' : 'English',
  'ISO-639-1' : 'en'
}

msg = {    
  'te_received_cmd'         : ["Received command: '{0}'"],  
  'te_delete_db'            : ["Deleting database: '{0}'"],
  'te_create_db'            : ["Creating database: '{0}'"],
  'te_install_db'           : ["Installing database from script: '{0}'"],
  'te_db_installed'         : ["Database installed successfully"],
  'te_unknown_install'      : ["Unknown installation script"],
  'te_web_unknown_file'     : ["Unknown file: '{0}'"],
  'te_db_connected'         : ["Successfully connected to database"],
  'te_db_disconnected'      : ["Disconnected from database"],
  'te_db_func'              : ["Calling DB function: '{0}' with params: '{1}'"],
  'te_db_unknown_entity'    : ["Unknown entity: '{0}' with ID: '{1}'"],
  'te_db_entity_found'      : ["Found entity: '{0}' with params: '{1}'"],
  'te_db_entity_created'    : ["Created entity: '{0}' with ID: '{1}'"],
  'te_db_entity_changed'    : ["Changed entity: '{0}' with ID: '{1}'"],
  'te_db_role_assigned'     : ["Assigned role to entity: '{0}'"],
  'te_db_role_revoked'      : ["Revoked role from entity: '{0}'"],
  'te_db_srv_forbidden'     : ["Service: '{0}' is forbidden for entity: '{1}'"],
  'te_db_srv_assigned'      : ["Service: '{0}' is already assigned"],
  'te_db_unknown_srv_param' : ["Service: '{0}' has not allowed param: '{1}'"],
  'te_db_mandatory_param'   : ["Param: '{0}' is mandatory"],
  'te_db_param_not_assigned': ["Param: '{0}' id not assigned"],
  'te_rest_request'         : ["Received REST request: '{0}' with data: '{1}'"],
  'te_rest_func'            : ["Calling REST function: '{0}' with params: '{1}'"],
  'te_rest_unknown_entity'  : ["Unknown entity: '{0}' with ID: '{1}'"],
  'te_rest_entity_found'    : ["Found entity: '{0}' with params: '{1}'"],
  'te_rest_entity_created'  : ["Created entity: '{0}' with ID: '{1}'"],
  'te_rest_entity_changed'  : ["Changed entity: '{0}' with ID: '{1}'"],  
  'te_rest_role_assigned'   : ["Role assigned to entity: '{0}'"],
  'te_rest_role_revoked'    : ["Role revoked from entity: '{0}'"],  
  'te_soap_request'         : ["Received SOAP request: '{0}' with data: '{1}'"],  
  'te_soap_func'            : ["Calling SOAP function: '{0}' with params: '{1}'"],
  'te_soap_unknown_entity'  : ["Unknown entity: '{0}' with ID: '{1}'"],
  'te_soap_entity_found'    : ["Found entity: '{0}' with params: '{1}'"],
  'te_soap_entity_created'  : ["Created entity: '{0}' with ID: '{1}'"],
  'te_soap_entity_changed'  : ["Changed entity: '{0}' with ID: '{1}'"],    
  'te_soap_role_assigned'   : ["Role assigned to entity: '{0}'"],
  'te_soap_role_revoked'    : ["Role revoked from entity: '{0}'"]     
}
