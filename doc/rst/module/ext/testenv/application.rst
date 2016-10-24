.. _module_ext_testenv_application:

Application
===========

This sections contains module documentation of testenv application modules.

Data model
^^^^^^^^^^

**Customer structure**

 .. graphviz::
   
   digraph customer_structure {
      graph [rankdir=TB]
      node [shape=box, style=filled, color=white, fillcolor=lightgrey]
    
      customer
      payer
      subscriber
      lov_status
      lov_segment
      lov_billcycle
      lov_market
      lov_lov_tariff
      
      customer -> payer
      customer -> subscriber
      payer -> subscriber
      lov_status -> customer
      lov_status -> payer
      lov_status -> subscriber
      lov_segment -> customer
      lov_billcycle -> payer
      lov_market -> subscriber
      lov_tariff -> subscriber

   }
   
**Contact and address**

 .. graphviz::
   
   digraph contact_and_address {
      graph [rankdir=TB]
      node [shape=box, style="filled", color=white, fillcolor=lightgrey]
    
      customer
      payer
      subscriber
      contact
      contact_role
      address
      address_role
      lov_contact_role
      lov_address_role
      
      contact -> contact_role
      customer -> contact_role
      payer -> contact_role
      subscriber -> contact_role
      address -> address_role
      contact -> address_role
      customer -> address_role
      payer -> address_role
      subscriber -> address_role
      lov_contact_role -> contact_role
      lov_address_role -> address_role
        
   }
   
**Services**

 .. graphviz::
   
   digraph contact_and_address {
      graph [rankdir=TB]
      node [shape=box, style="filled", color=white, fillcolor=lightgrey]
    
      customer
      payer
      subscriber
      service
      service_params
      lov_service
      lov_service_params
      lov_status
      
      customer -> service
      payer -> service
      subscriber -> service
      service -> service_params
      lov_service -> service
      lov_service_param -> service_params
      lov_status -> service
        
   }   
   
Database tables
^^^^^^^^^^^^^^^

**customer**:

Storage of customers

===========  ======== ======== =============================
Column       Datatype Nullable Constraint 
===========  ======== ======== =============================
id           integer     N     primary key autoincrement
name         varchar     N
status       integer     N     foreign key to lov_status.id
segment      integer     N     foreign key to lov_segment.id
birth_no     varchar     Y
reg_no       varchar     Y
tax_no       varchar     Y
create_date  datetime    Y
modify_date  datetime    Y
===========  ======== ======== =============================

**payer**:

Storage of payers

============  ======== ======== ===============================
Column        Datatype Nullable Constraint 
============  ======== ======== ===============================
id            integer     N     primary key autoincrement
name          varchar     N
status        integer     N     foreign key to lov_status.id
billcycle     integer     N     foreign key to lov_billcycle.id
bank_account  varchar     Y
customer      integer     N     foreign key to customer.id
create_date   datetime    Y
modify_date   datetime    Y
============  ======== ======== ===============================

**subscriber**:

Storage of subscribers

===========  ======== ======== =============================
Column       Datatype Nullable Constraint 
===========  ======== ======== =============================
id           integer     N     primary key autoincrement
name         varchar     N
msisdn       varchar     N
status       integer     N     foreign key to lov_status.id
market       integer     N     foreign key to lov_segment.id
tariff       varchar     N     foreign key to lov_tariff.id
customer     integer     N     foreign key to customer.id
payer        integer     N     foreign key to payer.id
create_date  datetime    Y
modify_date  datetime    Y
===========  ======== ======== =============================

**contact**:

Storage of contacts

===========  ======== ======== =============================
Column       Datatype Nullable Constraint 
===========  ======== ======== =============================
id           integer     N     primary key autoincrement
name         varchar     N
phone        varchar     Y
email        varchar     Y
create_date  datetime    Y
modify_date  datetime    Y
===========  ======== ======== =============================

**contact_role**:

Storage of contact roles

============  ======== ======== ==================================
Column        Datatype Nullable Constraint 
============  ======== ======== ==================================
id            integer     N     primary key autoincrement
contact_role  integer     N     foreign key to lov_contact_role.id
contact       integer     N     foreign key to contact.id
customer      integer     Y     foreign key to customer.id
payer         integer     Y     foreign key to payer.id
subscriber    integer     Y     foreign key to subscriber.id
create_date   datetime    Y
============  ======== ======== ==================================

**address**:

Storage of addresses

===========  ======== ======== =============================
Column       Datatype Nullable Constraint 
===========  ======== ======== =============================
id           integer     N     primary key autoincrement
street       varchar     N
street_no    varchar     N
city         varchar     N
zip          integer     N
create_date  datetime    Y
modify_date  datetime    Y
===========  ======== ======== =============================

**address_role**:

Storage of address roles

============  ======== ======== ==================================
Column        Datatype Nullable Constraint 
============  ======== ======== ==================================
id            integer     N     primary key autoincrement
address_role  integer     N     foreign key to lov_address_role.id
address       integer     N     foreign key to address.id
contact       integer     Y     foreign key to contact.id
customer      integer     Y     foreign key to customer.id
payer         integer     Y     foreign key to payer.id
subscriber    integer     Y     foreign key to subscriber.id
create_date   datetime    Y
============  ======== ======== ==================================

**service**:

Storage of services

===========  ======== ======== =============================
Column       Datatype Nullable Constraint 
===========  ======== ======== =============================
id           integer     N     primary key autoincrement
service      integer     N     foreign key to lov_service.id
status       integer     N     foreign key to lov_status.id
customer     integer     Y     foreign key to customer.id
payer        integer     Y     foreign key to payer.id
subscriber   integer     Y     foreign key to subscriber.id
create_date  datetime    Y
modify_date  datetime    Y
===========  ======== ======== =============================

**service_params**:

Storage of service parameters

===========  ======== ======== ===================================
Column       Datatype Nullable Constraint 
===========  ======== ======== ===================================
id           integer     N     primary key autoincrement
param        integer     N     foreign key to lov_service_param.id
value        varchar     Y
service      integer     N     foreign key to lov_service.id
create_date  datetime    Y
modify_date  datetime    Y
===========  ======== ======== ===================================

**history**:

Auditing table, operation with every entity is logged.

===========  ======== ======== =========================
Column       Datatype Nullable Constraint 
===========  ======== ======== =========================
id           integer     N     primary key autoincrement
event_date   datetime    N
table_name   varchar     N
table_id     integer     N
event        varchar     N
log          clob        Y
===========  ======== ======== =========================

**lov_status**:

List of statuses

===========  ======== ======== ===========
Column       Datatype Nullable Constraint 
===========  ======== ======== ===========
id           integer     N     primary key
title        varchar     N
===========  ======== ======== ===========

Following statuses are configured

== ========
id title
== ========
1  active
2  deactive
3  suspend
== ========

**lov_segment**:

List of customer segments

===========  ======== ======== ===========
Column       Datatype Nullable Constraint 
===========  ======== ======== ===========
id           integer     N     primary key
title        varchar     N
===========  ======== ======== ===========

Following segment are configured

== =====
id title
== =====
2  RES
3  VSE
4  SME
5  LE
== =====

**lov_billcycle**:

List of payer billcycles

===========  ======== ======== ===========
Column       Datatype Nullable Constraint 
===========  ======== ======== ===========
id           integer     N     primary key
title        varchar     N
===========  ======== ======== ===========

Following billcycles are configured

== =====
id title
== =====
1  51
2  52
3  53
4  54
== =====

**lov_market**:

List of subscriber markets

===========  ======== ======== ===========
Column       Datatype Nullable Constraint 
===========  ======== ======== ===========
id           integer     N     primary key
title        varchar     N
===========  ======== ======== ===========

Following statuses are configured

== =====
id title
== =====
1  GSM
2  DSL
3  FIX
== =====

**lov_tariff**:

List of subscriber tariffs

===========  ======== ======== ===========
Column       Datatype Nullable Constraint 
===========  ======== ======== ===========
id           integer     N     primary key
title        varchar     N
segment      integer     Y
market       integer     Y
monthly_fee  integer     Y
===========  ======== ======== ===========

Following tariffs are configured

=== ========================================
id  title
=== ========================================
433 S nami sit nesit
459 S nami sit nesit bez zavazku
434 S nami sit nesit v podnikani
460 S nami sit nesit v podnikani bez zavazku
=== ========================================

**lov_contact_role**:

List of contact roles

===========  ======== ======== ===========
Column       Datatype Nullable Constraint 
===========  ======== ======== ===========
id           integer     N     primary key
title        varchar     N
===========  ======== ======== ===========

Following roles are configured

== =========
id title
== =========
1  contact
2  contract
3  invoicing
== =========

**lov_address_role**:

List od address roles

===========  ======== ======== ===========
Column       Datatype Nullable Constraint 
===========  ======== ======== ===========
id           integer     N     primary key
title        varchar     N
===========  ======== ======== ===========

Following roles are configured

== =========
id title
== =========
1  contact
2  contract
3  invoicing
4  delivery
== =========

**lov_service**:

List of services

===========  ======== ======== ===========
Column       Datatype Nullable Constraint 
===========  ======== ======== ===========
id           integer     N     primary key
title        varchar     N
monthly_fee  integer     Y
customer     integer     Y
payer        integer     Y
subscriber   integer     Y
===========  ======== ======== ===========

Following services are configured

=== =============== ======== ===== ==========
id  title           customer payer subscriber
=== =============== ======== ===== ==========
615 Telefonni cislo    0       0       1 
619 SIM karta          0       0       1
=== =============== ======== ===== ==========

**lov_service_param**:

List of service parameters

=============  ======== ======== =============================
Column         Datatype Nullable Constraint 
=============  ======== ======== =============================
id             integer     N     primary key
title          varchar     N
service        integer     N     foreign key to lov_service.id
default_value  varchar     Y
mandatory      integer     Y
=============  ======== ======== =============================

Following parameters are configured

Following statuses are configured

=== ======== ======= =========
id  title    service mandatory
=== ======== ======= =========
121 MSISDN   615         1
122 ICCID    619         1
123 IMSI     619         1
=== ======== ======= =========

entities
^^^^^^^^

Module provides classes for all entities modeled in database. 

* Customer - table customer
* Payer - table payer
* Subscriber - table subscriber
* Contact - table contact
* ContactRole - table contact_role
* Address - table address
* AddressRole - table address_role
* Service - tables service, service_params
* ServiceOperation - auxiliary class for manipulation with service

Each class implements same methods.

* __init__ - set all attributes
* __str__ - serialization to string
* toxml - serialization to xml object (lxml.etree)
* tojson - serialization to json string

db_handler
^^^^^^^^^^

Module provides interface for database implemented in SQLite. It uses module hydratk.lib.network.dbi.client
which is automatically installed. 

**Attributes** :

* _mh - MasterHead reference
* _db_file - database filename
* _client - DBClient instance

**Methods** :

* connect 

Method connects to database.

* disconnect 

Method disconnect from database.

* customer

Methods for manipulation with customer entity. Method read_customer selects from table customer. Method create_customer inserts to tables customer and history, 
status is translated to id from table lov_status. Method change_customer updates in table customer and inserts to history.

* payer

Methods for manipulation with payer entity. Method read_payer selects from table payer. Method create_payer inserts to tables payer and history, 
status is translated to id from table status. Method change_payer updates in table payer and inserts to history.

* subscriber

Methods for manipulation with subscriber entity. Method read_subscriber selects from table subscriber. Method create_subscriber inserts to tables subscriber and history, 
status is translated to id from table status. Method change_subscriber updates in table subscriber and inserts to history.

* contact

Methods for manipulation with contact entity. Method read_contact selects from table contact and contact_role (if assigned). Role titles are translated
from table lov_contact_role. Method create_contact inserts to tables contact and history. Method change_contact updates in table contact and inserts to history.
Method assign_contact_role inserts to tables contact_role and history. Method revoke_contact_role deletes from table contact_role and inserts to history.

* address

Methods for manipulation with address entity. Method read_address selects from table address and address (if assigned). Role titles are translated
from table lov_address_role. Method create_address inserts to tables address and history. Method change_address updates in table address and inserts to history.
Method assign_address_role inserts to tables address_role and history. Method revoke_address_role deletes from table address_role and inserts to history.

* service

Methods for manipulation with service entity. Method read_services selects from tables service and service_params. Method creates_service inserts to tables 
service, service_params and history. It checks whether service is allowed for customer,payer,subscriber in table lov_service and checks if service is already 
assigned in table service. It reads allowed and mandatory parameters from table lov_service_param. Method change_service updates in tables service and service_params and inserts to history.

web_server
^^^^^^^^^^

Module provides web server with REST and SOAP services implemented using external module `web.py <http://webpy.org/>`_ in version >= 0.37.
When Python3 is used the module replaced by different branch `py3 <https://github.com/webpy/webpy.git@py3#egg=webpy>`_.

Module contains several classes.

* Server

Starts web server on configured IP address (0.0.0.0) and port (default 8888) using web.py methods application, runsimple, wsgifunc.

* Index

Handles GET request on / and returns Hello, World.

* Customer

Handles GET, POST, PUT requests on /rs/customer and routes them to RestHandler. 

* Payer

Handles GET, POST, PUT requests on /rs/payer and routes them to RestHandler.

* Subscriber

Handles GET, POST, PUT requests on /rs/subscriber and routes them to RestHandler.

* Contact

Handles GET, POST, PUT requests on /rs/contact and routes them to RestHandler.

* ContactRole

Handles POST, PUT requests on /rs/contact/role and routes them to RestHandler.

* Address

Handles GET, POST, PUT requests on /rs/address and routes them to RestHandler.

* AddressRole

Handles POST, PUT requests on /rs/address/role and routes them to RestHandler.

* Service

Handles GET, POST, PUT requests on /rs/service and routes them to RestHandler.

* SoapService

Handles GET, POST requests on /ws/crm. GET request returns content of WSDL (crm.wsdl) or XSD (crm.xsd) if URL parameter wsdl of xsd is provided.
File location is configured. POST request is routed to SoapHandler.

RestHandler
^^^^^^^^^^^

Module provides class RestHandler with REST service. Each entity method uses appropriate method in DbHandler.
It uses simplejson method loads to read JSON and entity method tojson to write JSON. 

**Attributes** :

* _mh - MasterHead reference

**Methods** :

* __init__

Method sets MasterHead reference.

* _get_db

Method gets initializes DbHandler and connects to database.

* customer

Methods for manipulation with customer entity - read_customer, create_customer, change_customer.

* payer

Methods for manipulation with payer entity - read_payer, create_payer, change_payer.

* subscriber

Methods for manipulation with subscriber entity - read_subscriber, create_subscriber, change_subscriber.

* contact

Methods for manipulation with contact entity - read_contact, create_contact, change_contact, assign_contact_role, revoke_contact_role.

* address

Methods for manipulation with address entity - read_address, create_address, change_address, assign_address_role, revoke_address_role.

* service

Methods for manipulation with service entity - read_services, create_service, change_service.

SoapHandler
^^^^^^^^^^^

Module provides class SoapHandler with SOAP service. Each entity method uses appropriate method in DbHandler.
It uses lxml method objectify.fromstring to read XML entity method toxml and lxml method tostring to write XML. 

**Attributes** :

* _mh - MasterHead reference
* _nsmap - namespace map
* _ns0 - SOAP namespace
* _ns1 - application namespace

**Methods** :

* __init__

Method sets MasterHead reference and namespaces.

* _get_db

Method gets initializes DbHandler and connects to database.

* _fault

Method prepares SOAP Fault response.

* _response

Method prepares SOAP standard response.

* dispatcher

Method dispatches request according to HTTP header SOAPAction.

* customer

Methods for manipulation with customer entity - read_customer, create_customer, change_customer.

* payer

Methods for manipulation with payer entity - read_payer, create_payer, change_payer.

* subscriber

Methods for manipulation with subscriber entity - read_subscriber, create_subscriber, change_subscriber.

* contact

Methods for manipulation with contact entity - read_contact, create_contact, change_contact, assign_contact_role, revoke_contact_role.

* address

Methods for manipulation with address entity - read_address, create_address, change_address, assign_address_role, revoke_address_role.

* service

Methods for manipulation with service entity - read_services, create_service, change_service.

Unit tests
^^^^^^^^^^

Application modules have no specific unit tests. Extension TestEnv also serves as tutorial how to write test libraries/helpers and scripts for Yoda extension.
These scripts are used as unit tests.

**lib** :

* db_int

Module provides class DB_INT with methods to test all operations in database. The methods directly call appropriate DBHandler methods.

* rest_int

Module provides class REST_INT with methods to test all operations in REST service. It uses hydratk.lib.network.rest.client.RESTClient.

* soap_int 

Module provides class SOAP_INT with methods to test all operations in SOAP service. It uses hydratk.lib.network.rest.client.SOAPClient.

**helpers** :

* helpers

Imports libraries DB_INT, REST_INT, SOAP_INT to be accessible in test scripts.

**tests** :

* db

  .. code-block:: python      
  
    # initialize client 
    import yodahelpers.hydratk.extensions.testenv.helpers as hlp
    client = hlp.db()
    res = client.connect()
    
    # create customer
    name = 'Vince Neil'
    status = 'active'
    segment = 2
    birth_no = '700101/0001'
    reg_no = '12345'
    tax_no = 'CZ12345'
    cust = client.create_customer(name, segment, status, birth_no, reg_no, tax_no)   
    customer = client.read_customer(cust)   

* rest

  .. code-block:: python

    # initialize client
    import yodahelpers.hydratk.extensions.testenv.helpers as hlp    
    client = hlp.rest()
    
    # create customer
    name = 'Vince Neil'
    status = 'active'
    segment = 2
    birth_no = '700101/0001'
    reg_no = '12345'
    tax_no = 'CZ12345'
    cust = client.create_customer(name, segment, status, birth_no, reg_no, tax_no)  
    customer = client.read_customer(cust)    

* soap

  .. code-block:: python
  
     # initialize client
     import yodahelpers.hydratk.extensions.testenv.helpers as hlp
     client = hlp.soap()     
     
     # create customer
     
     name = 'Vince Neil'
     status = 'active'
     segment = 2
     birth_no = '700101/0001'
     reg_no = '12345'
     tax_no = 'CZ12345'
     cust = client.create_customer(name, segment, status, birth_no, reg_no, tax_no) 
     customer = client.read_customer(cust)      