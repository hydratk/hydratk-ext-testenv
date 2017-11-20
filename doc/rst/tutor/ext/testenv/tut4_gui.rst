.. _tutor_testenv_tut4_gui:

Tutorial 4: GUI interface
=========================

Sample Yoda script is located in /var/local/hydratk/yoda/yoda-tests/hydratk/extensions/testenv/sys_gui.jedi.
Sample smoke test is located in smoke.jedi.
Sample integration test (GUI+DB) in located in int_gui.jedi, it uses helpers for different interfaces.

Important snippets are commented.

Open
^^^^

  .. code-block:: python
  
     # import helpers
     import yodahelpers.hydratk.extensions.testenv.helpers as hlp
    
     # create GUI client instance and open browser
     client = hlp.db()
     res = client.open() # returns bool
     
Close
^^^^^

  .. code-block:: python
  
     # returns bool
     client.close()     

Customer
^^^^^^^^

  .. code-block:: python
  
     # create customer
     name = 'Vince Neil'
     status = 'active'
     segment = 'RES'
     birth_no = '700101/0001'
     reg_no = '12345'
     tax_no = 'CZ12345'
     
     # returns generated id
     cust = client.create_customer(name, status, segment, birth_no, reg_no, tax_no)
     
     # read created customer, returns Customer object
     print client.read_customer(cust) 
     # id:1|name:Vince Neil|status:active|segment:RES|birth_no:700101/0001|reg_no:12345|tax_no:CZ12345
     
     # change customer
     name = 'Charlie Bowman'
     status = 'suspend'
     segment = 'VSE'
     birth_no = '700101/0002'
     reg_no = '1234'
     tax_no = 'CZ1234'
     
     # returns bool
     res = client.change_customer(cust, name, status, segment, birth_no, reg_no, tax_no)   
     
Payer
^^^^^

  .. code-block:: python
  
     # create payer
     name = 'Vince Neil'
     status = 'active'
     billcycle = '51'
     bank_account = '123456/0100'
     customer = cust
     
     # returns generated id
     pay = client.create_payer(name, status, billcycle, customer, bank_account) 
     
     # read created payer, returns Payer object
     print client.read_payer(pay)
     # id:1|name:Vince Neil|status:active|billcycle:51|bank_account:123456/0100|customer:1
     
     # change payer
     name = 'Charlie Bowman'
     status = 'suspend'
     billcycle = '52'
     bank_account = '654321/0800'
     
     # returns bool
     res = client.change_payer(pay, name, status, billcycle, bank_account)  
     
Subscriber
^^^^^^^^^^

  .. code-block:: python
  
     # create subscriber
     name = 'Vince Neil'
     msisdn = '773592179'
     status = 'active'
     market = 'GSM'
     tariff = 'S nami sit nesit'
     customer = cust
     payer = pay
     
     # returns generated id
     subs = client.create_subscriber(name, msisdn, market, tariff, customer, payer, status)
     
     # read created subscriber, returns Subscriber object
     print client.read_subscriber(subs)                             
     # id:1|name:Vince Neil|msisdn:773592179|status:active|market:GSM|tariff:S nami sit nesit|customer:1|payer:1
     
     # change subscriber
     name = 'Charlie Bowman'
     msisdn = '603404746'
     status = 'suspend'
     market = 'DSL'
     tariff = 'S nami sit nesit v podnikani'
     
     # returns bool
     res = client.change_subscriber(subs, name, msisdn, status, market, tariff)
     
Contact
^^^^^^^

  .. code-block:: python
  
     # create contact
     name = 'Vince Neil'
     phone = '12345'
     email = 'aaa@xxx.com'
     
     # returns generated id
     con = client.create_contact(name, phone, email)
     
     # read created contact, returns Contact object
     client.read_contact(con)  
     # id:1|name:Vince Neil|phone:12345|email:aaa@xxx.com|roles#
     
     # change contact
     name = 'Charlie Bowman'
     phone = '123456'
     email = 'bbb@xxx.com'
     
     # returns bool
     res = client.change_contact(con, name, phone, email) 
     
     # assign contact role
     # returns bool
     client.assign_contact_role(con, 'contract', customer=cust)  
     client.assign_contact_role(con, 'invoicing', payer=pay) 
     client.assign_contact_role(con, 'contact', subscriber=subs)    
     
     # read contact with roles
     print client.read_contact(con)
     # id:1|name:Charlie Bowman|phone:123456|email:bbb@xxx.com|roles#id:1|title:contract|customer:1|payer:None|subscriber:None
     # id:1|title:invoicing|customer:None|payer:1|subscriber:None#id:1|title:contact|customer:None|payer:None|subscriber:1# 
       
     # revoke contact role
     # returns bool
     client.revoke_contact_role(con, 'contract', customer=cust)  
     client.revoke_contact_role(con, 'invoicing', payer=pay) 
     client.revoke_contact_role(con, 'contact', subscriber=subs) 
     
Address
^^^^^^^

  .. code-block:: python
  
     # create address
     street = 'Tomickova'
     street_no = '2144/1'
     city = 'Praha'
     zip = 14900
     
     # returns generated id
     addr = client.create_address(street, street_no, city, zip)  
     
     # read cread address, returns Address object
     # id:1|street:Tomickova|street_no:2144/1|city:Praha|zip:14900|roles#
     
     # change address
     street = 'Babakova'
     street_no = '2152/6'
     city = 'Praha 4'
     zip = 14800
     
     # returns bool
     client.change_address(addr, street, street_no, city, zip)  
     
     # assign address role
     # returns bool
     client.assign_address_role(addr, 'contract', customer=cust)  
     client.assign_address_role(addr, 'invoicing', payer=pay) 
     client.assign_address_role(addr, 'contact', subscriber=subs) 
     client.assign_address_role(addr, 'delivery', contact=con)    
     
     # read address with roles
     print client.read_address(addr)
     # id:1|street:Babakova|street_no:2152/6|city:Praha 4|zip:14800|roles#id:1|title:contract|contact:None|customer:1|payer:None|subscriber:None
     # id:1|title:invoicing|contact:None|customer:None|payer:1|subscriber:None#id:1|title:contact|contact:None|customer:None|payer:None|subscriber:1
     # id:1|title:delivery|contact:1|customer:None|payer:None|subscriber:None#   
       
     # revoke address role
     # returns bool
     client.revoke_address_role(addr, 'contract', customer=cust)  
     client.revoke_address_role(addr, 'invoicing', payer=pay) 
     client.revoke_address_role(addr, 'contact', subscriber=subs)  
     client.revoke_address_role(addr, 'delivery', contact=con)  
         