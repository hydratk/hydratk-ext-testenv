# -*- coding: utf-8 -*-
"""Handles GUI operations

.. module:: testenv.gui_handler
   :platform: Unix
   :synopsis: Handles GUI operations
.. moduleauthor:: Petr Rašek <bowman@hydratk.org>

"""

from hydratk.core.masterhead import MasterHead
from hydratk.extensions.testenv.db_handler import DbHandler
from web.template import render
from web.form import Form, Hidden, Textbox, Dropdown, Button
from os import path

class GuiHandler(object):
    """Class GuiHandler
    """

    _mh = None
    _tmpl = None
    _lovs = {}
    _data = {}
    _current_tab = 'tCustomer'

    def __init__(self):
        """Class constructor

        Called when the object is initialized

        Args:
           none

        """

        self._mh = MasterHead.get_head()
        self._tmpl = render(path.join(path.dirname(__file__), 'templates'))
        self._lovs = self._load_lovs()
        self._init_data()

    def _get_db(self):
        """Method connect to database

        Args:
           none

        Returns:
           obj: DB client

        """

        db = DbHandler()
        db.connect()
        return db

    def _load_lovs(self):
        """Method loads LOVs from database

        Args:
           none

        Returns:
           dict

        """

        db = self._get_db()
        lovs = {
                'status'       : db.get_lov('status'),
                'segment'      : db.get_lov('segment'),
                'billcycle'    : db.get_lov('billcycle'),
                'market'       : db.get_lov('market'),
                'tariff'       : db.get_lov('tariff'),
                'contact_role' : db.get_lov('contact_role'),
                'address_role' : db.get_lov('address_role')
               }
        db.disconnect()

        return lovs

    def _init_data(self):
        """Method sets initial data

        Args:
           none

        Returns:
           void

        """
        
        self._data = {
                      'customer' : {
                        'id'       : '',
                        'name'     : '',
                        'status'   : '',
                        'segment'  : '',
                        'birth_no' : '',
                        'reg_no'   : '',
                        'tax_no'   : ''
                      },
                      'payer' : {
                        'id'           : '',
                        'name'         : '',
                        'status'       : '',
                        'billcycle'    : '',
                        'bank_account' : '',
                        'customer'     : ''
                      },
                      'subscriber' : {
                        'id'       : '',
                        'name'     : '',
                        'msisdn'   : '',
                        'status'   : '',
                        'market'   : '',
                        'tariff'   : '',
                        'customer' : '',
                        'payer'    : ''
                      },
                      'contact' : {
                        'id'         : '',
                        'name'       : '',
                        'phone'      : '',
                        'email'      : ''
                      },
                      'contact_role' : {
                        'title'      : '',
                        'customer'   : '',
                        'payer'      : '',
                        'subscriber' : '',
                        'roles'      : []
                      },
                      'address' : {
                        'id'         : '',
                        'street'     : '',
                        'street_no'  : '',
                        'city'       : '',
                        'zip'        : ''
                      },
                      'address_role' : {
                        'title'      : '',
                        'contact'    : '',
                        'customer'   : '',
                        'payer'      : '',
                        'subscriber' : '',
                        'roles'      : []
                      }
                     }
        
    def _store_data(self):
        """Method stores current data

        Args:
           none

        Returns:
           obj

        """
        
        self._data = {
                      'customer' : {
                        'id'       : self._customerId.get_value(),
                        'name'     : self._customerName.get_value(),
                        'status'   : self._customerStatus.get_value(),
                        'segment'  : self._customerSegment.get_value(),
                        'birth_no' : self._customerBirthNumber.get_value(),
                        'reg_no'   : self._customerRegistrationNumber.get_value(),
                        'tax_no'   : self._customerTaxNumber.get_value()
                      },
                      'payer' : {
                        'id'           : self._payerId.get_value(),
                        'name'         : self._payerName.get_value(),
                        'status'       : self._payerStatus.get_value(),
                        'billcycle'    : self._payerBillcycle.get_value(),
                        'bank_account' : self._payerBankAccount.get_value(),
                        'customer'     : self._payerCustomer.get_value()
                      },
                      'subscriber' : {
                        'id'       : self._subscriberId.get_value(),
                        'name'     : self._subscriberName.get_value(),
                        'msisdn'   : self._subscriberMsisdn.get_value(),
                        'status'   : self._subscriberStatus.get_value(),
                        'market'   : self._subscriberMarket.get_value(),
                        'tariff'   : self._subscriberTariff.get_value(),
                        'customer' : self._subscriberCustomer.get_value(),
                        'payer'    : self._subscriberPayer.get_value()
                      },
                      'contact' : {
                        'id'         : self._contactId.get_value(),
                        'name'       : self._contactName.get_value(),
                        'phone'      : self._contactPhone.get_value(),
                        'email'      : self._contactEmail.get_value()
                      },
                      'contact_role' : {
                        'title'      : self._contactRoleTitle.get_value(),
                        'customer'   : self._contactRoleCustomer.get_value(),
                        'payer'      : self._contactRolePayer.get_value(),
                        'subscriber' : self._contactRoleSubscriber.get_value(),
                        'roles'      : self._contactRoleRoles
                      },
                      'address' : {
                        'id'         : self._addressId.get_value(),
                        'street'     : self._addressStreet.get_value(),
                        'street_no'  : self._addressStreetNumber.get_value(),
                        'city'       : self._addressCity.get_value(),
                        'zip'        : self._addressZip.get_value()
                      },
                      'address_role' : {
                        'title'      : self._addressRoleTitle.get_value(),
                        'contact'    : self._addressRoleContact.get_value(),
                        'customer'   : self._addressRoleCustomer.get_value(),
                        'payer'      : self._addressRolePayer.get_value(),
                        'subscriber' : self._addressRoleSubscriber.get_value(),
                        'roles'      : self._addressRoleRoles
                      }
                     }

    def _translate_lov(self, lov, id=None, title=None):
        """Method translates LOV id <-> title

        Args:
           lov (str): LOV
           id (int): translate id to title
           title (str): translate title to id

        Returns:
           int or str

        """

        if (id != None):
            for rec in self._lovs[lov]:
                if (rec[0] == id):
                    result = rec[1]
        else:
            for rec in self._lovs[lov]:
                if (rec[1] == title):
                    result = rec[0]

        return result
    
    def render_page(self, data={}):
        """Method renders page

        Args:
           data (dict): POST data

        Returns:
           str

        """



        if ('customer' in data or 'payer' in data or 'subscriber' in data):
            self._current_tab = 'tCustomer'
        elif ('contact' in data or 'contact_role' in data or 'address' in data or 'address_role' in data):
            self._current_tab = 'tContact'

        kwargs = {
                  'currentTab'  : self._current_tab,
                  'customer'    : {
                                   'form'    : self._init_customer_form(),
                                   'buttons' : [self._customerRead, self._customerCreate, self._customerChange]
                                  },
                  'payer'       : {
                                   'form'    : self._init_payer_form(),
                                   'buttons' : [self._payerRead, self._payerCreate, self._payerChange]
                                  },
                  'subscriber'  : {
                                   'form'    : self._init_subscriber_form(),
                                   'buttons' : [self._subscriberRead, self._subscriberCreate, self._subscriberChange]
                                  },
                  'contact'     : {
                                   'form'    : self._init_contact_form(),
                                   'buttons' : [self._contactRead, self._contactCreate, self._contactChange]
                                  },
                  'contactRole' : {
                                   'form'    : self._init_contact_role_form(),
                                   'buttons' : [self._contactRoleAssign, self._contactRoleRevoke],
                                   'roles'   : self._contactRoleRoles
                                  },
                  'address'     : {
                                   'form'    : self._init_address_form(),
                                   'buttons' : [self._addressRead, self._addressCreate, self._addressChange]
                                  },
                  'addressRole' : {
                                   'form'    : self._init_address_role_form(),
                                   'buttons' : [self._addressRoleAssign, self._addressRoleRevoke],
                                   'roles'   : self._addressRoleRoles
                                  }
                 }

        if (data == {}):
            return self._tmpl.main(kwargs)

        if ('customer' in data):
            if ('customerRead' in data):
                self._read_customer(data)
            elif ('customerCreate' in data):
                self._create_customer(data)
            elif ('customerChange' in data):
                self._change_customer(data)
        elif ('payer' in data):
            if ('payerRead' in data):
                self._read_payer(data)
            elif ('payerCreate' in data):
                self._create_payer(data)
            elif ('payerChange' in data):
                self._change_payer(data)
        elif ('subscriber' in data):
            if ('subscriberRead' in data):
                self._read_subscriber(data)
            elif ('subscriberCreate' in data):
                self._create_subscriber(data)
            elif ('subscriberChange' in data):
                self._change_subscriber(data)
        elif ('contact' in data):
            if ('contactRead' in data):
                self._read_contact(data)
                kwargs['contactRole']['roles'] = self._contactRoleRoles
            elif ('contactCreate' in data):
                self._create_contact(data)
            elif ('contactChange' in data):
                self._change_contact(data)
            elif ('contactRoleAssign' in data):
                self._assign_contact_role(data)
                kwargs['contactRole']['roles'] = self._contactRoleRoles
            elif ('contactRoleRevoke' in data):
                self._revoke_contact_role(data)
                kwargs['contactRole']['roles'] = self._contactRoleRoles
        elif ('address' in data):
            if ('addressRead' in data):
                self._read_address(data)
                kwargs['addressRole']['roles'] = self._addressRoleRoles
            elif ('addressCreate' in data):
                self._create_address(data)
            elif ('addressChange' in data):
                self._change_address(data)
            elif ('addressRoleAssign' in data):
                self._assign_address_role(data)
                kwargs['addressRole']['roles'] = self._addressRoleRoles
            elif ('addressRoleRevoke' in data):
                self._revoke_address_role(data)
                kwargs['addressRole']['roles'] = self._addressRoleRoles

        self._store_data()

        return self._tmpl.main(kwargs)
    
    def _init_customer_form(self):
        """Method renders customer form

        Args:
           none

        Returns:
           obj

        """

        data = self._data['customer']
        action = Hidden('customer')
        self._customerId = Textbox('customerId', description='ID', value=data['id'])
        self._customerName = Textbox('customerName', description='Name', value=data['name'])
        self._customerStatus = Dropdown('customerStatus', description='Status', args=self._lovs['status'], value=data['status'])
        self._customerSegment = Dropdown('customerSegment', description='Segment', args=self._lovs['segment'], value=data['segment'])
        self._customerBirthNumber = Textbox('customerBirthNumber', description='Birth number', value=data['birth_no'])
        self._customerRegistrationNumber = Textbox('customerRegistrationNumber', description='Registration number', value=data['reg_no'])
        self._customerTaxNumber = Textbox('customerTaxNumber', description='Tax number', value=data['tax_no'])
        self._customerRead = Button('customerRead', type='submit', html='Read')
        self._customerCreate = Button('customerCreate', type='submit', html='Create')
        self._customerChange = Button('customerChange', type='submit', html='Change')
        self._customerError = Textbox('customerError', description='Error', readonly=True)

        form = Form(
          action,
          self._customerId,
          self._customerName,
          self._customerStatus,
          self._customerSegment,
          self._customerBirthNumber,
          self._customerRegistrationNumber,
          self._customerTaxNumber,
          self._customerError
        )

        return form

    def _init_payer_form(self):
        """Method renders payer form

        Args:
           none

        Returns:
           obj

        """

        data = self._data['payer']
        action = Hidden('payer')
        self._payerId = Textbox('payerId', description='ID', value=data['id'])
        self._payerName = Textbox('payerName', description='Name', value=data['name'])
        self._payerStatus = Dropdown('payerStatus', description='Status', args=self._lovs['status'], value=data['status'])
        self._payerBillcycle = Dropdown('payerBillcycle', description='Billcycle', args=self._lovs['billcycle'], value=data['billcycle'])
        self._payerBankAccount = Textbox('payerBankAccount', description='Bank account', value=data['bank_account'])
        self._payerCustomer = Textbox('payerCustomer', description='Customer', value=data['customer'])
        self._payerRead = Button('payerRead', type='submit', html='Read')
        self._payerCreate = Button('payerCreate', type='submit', html='Create')
        self._payerChange = Button('payerChange', type='submit', html='Change')
        self._payerError = Textbox('payerError', description='Error', readonly=True)

        form = Form(
          action,
          self._payerId,
          self._payerName,
          self._payerStatus,
          self._payerBillcycle,
          self._payerBankAccount,
          self._payerCustomer,
          self._payerError
        )

        return form

    def _init_subscriber_form(self):
        """Method renders subscriber form

        Args:
           none

        Returns:
           obj

        """

        data = self._data['subscriber']
        action = Hidden('subscriber')
        self._subscriberId = Textbox('subscriberId', description='ID', value=data['id'])
        self._subscriberName = Textbox('subscriberName', description='Name', value=data['name'])
        self._subscriberMsisdn = Textbox('subscriberMsisdn', description='MSISDN', value=data['msisdn'])
        self._subscriberStatus = Dropdown('subscriberStatus', description='Status', args=self._lovs['status'], value=data['status'])
        self._subscriberMarket = Dropdown('subscriberMarket', description='Market', args=self._lovs['market'], value=data['market'])
        self._subscriberTariff = Dropdown('subscriberTariff', description='Tariff', args=self._lovs['tariff'], value=data['tariff'])
        self._subscriberCustomer = Textbox('subscriberCustomer', description='Customer', value=data['customer'])
        self._subscriberPayer = Textbox('subscriberPayer', description='Payer', value=data['payer'])
        self._subscriberRead = Button('subscriberRead', type='submit', html='Read')
        self._subscriberCreate = Button('subscriberCreate', type='submit', html='Create')
        self._subscriberChange = Button('subscriberChange', type='submit', html='Change')
        self._subscriberError = Textbox('subscriberError', description='Error', readonly=True)

        form = Form(
          action,
          self._subscriberId,
          self._subscriberName,
          self._subscriberMsisdn,
          self._subscriberStatus,
          self._subscriberMarket,
          self._subscriberTariff,
          self._subscriberCustomer,
          self._subscriberPayer,
          self._subscriberError
        )

        return form

    def _init_contact_form(self):
        """Method renders contact form

        Args:
           none

        Returns:
           obj

        """

        data = self._data['contact']
        action = Hidden('contact')
        self._contactId = Textbox('contactId', description='ID', value=data['id'])
        self._contactName = Textbox('contactName', description='Name', value=data['name'])
        self._contactPhone = Textbox('contactPhone', description='Phone', value=data['phone'])
        self._contactEmail = Textbox('contactEmail', description='Email', value=data['email'])
        self._contactRead = Button('contactRead', type='submit', html='Read')
        self._contactCreate = Button('contactCreate', type='submit', html='Create')
        self._contactChange = Button('contactChange', type='submit', html='Change')
        self._contactError = Textbox('contactError', description='Error', readonly=True)

        form = Form(
          action,
          self._contactId,
          self._contactName,
          self._contactPhone,
          self._contactEmail,
          self._contactError
        )

        return form

    def _init_contact_role_form(self):
        """Method renders contact role form

        Args:
           none

        Returns:
           obj

        """

        data = self._data['contact_role']
        self._contactRoleTitle = Dropdown('contactRoleTitle', description='Title', args=self._lovs['contact_role'], value=data['title'])
        self._contactRoleCustomer = Textbox('contactRoleCustomer', description='Customer', value=data['customer'])
        self._contactRolePayer = Textbox('contactRolePayer', description='Payer', value=data['payer'])
        self._contactRoleSubscriber = Textbox('contactRoleSubscriber', description='Subscriber', value=data['subscriber'])
        self._contactRoleAssign = Button('contactRoleAssign', type='submit', html='Assign')
        self._contactRoleRevoke = Button('contactRoleRevoke', type='submit', html='Revoke')
        self._contactRoleError = Textbox('contactRoleError', description='Error', readonly=True)
        self._contactRoleRoles = data['roles']

        form = Form(
          self._contactRoleTitle,
          self._contactRoleCustomer,
          self._contactRolePayer,
          self._contactRoleSubscriber,
          self._contactRoleError
        )

        return form

    def _init_address_form(self):
        """Method renders address form

        Args:
           none

        Returns:
           obj

        """

        data = self._data['address']
        action = Hidden('address')
        self._addressId = Textbox('addressId', description='ID', value=data['id'])
        self._addressStreet = Textbox('addressStreet', description='City', value=data['city'])
        self._addressStreetNumber = Textbox('addressStreetNumber', description='Street number', value=data['street_no'])
        self._addressCity = Textbox('addressCity', description='City', value=data['city'])
        self._addressZip = Textbox('addressZip', description='ZIP', value=data['zip'])
        self._addressRead = Button('addressRead', type='submit', html='Read')
        self._addressCreate = Button('addressCreate', type='submit', html='Create')
        self._addressChange = Button('addressChange', type='submit', html='Change')
        self._addressError = Textbox('addressError', description='Error', readonly=True)

        form = Form(
          action,
          self._addressId,
          self._addressStreet,
          self._addressStreetNumber,
          self._addressCity,
          self._addressZip,
          self._addressError
        )

        return form

    def _init_address_role_form(self):
        """Method renders address role form

        Args:
           none

        Returns:
           obj

        """

        data = self._data['address_role']
        self._addressRoleTitle = Dropdown('addressRoleTitle', description='Title', args=self._lovs['address_role'], value=data['title'])
        self._addressRoleContact = Textbox('addressRoleContact', description='Contact', value=data['customer'])
        self._addressRoleCustomer = Textbox('addressRoleCustomer', description='Customer', value=data['customer'])
        self._addressRolePayer = Textbox('addressRolePayer', description='Payer', value=data['payer'])
        self._addressRoleSubscriber = Textbox('addressRoleSubscriber', description='Subscriber', value=data['subscriber'])
        self._addressRoleAssign = Button('addressRoleAssign', type='submit', html='Assign')
        self._addressRoleRevoke = Button('addressRoleRevoke', type='submit', html='Revoke')
        self._addressRoleError = Textbox('addressRoleError', description='Error', readonly=True)
        self._addressRoleRoles = data['roles']

        form = Form(
          self._addressRoleTitle,
          self._addressRoleContact,
          self._addressRoleCustomer,
          self._addressRolePayer,
          self._addressRoleSubscriber,
          self._addressRoleError
        )

        return form

    def _read_customer(self, data):
        """Method reads customer

        Args:
           data (dict): POST data

        Returns:
           none

        """
        
        if (data['customerId'] == ''):
            self._customerError.set_value('ID is mandatory')
        else:
            id = int(data['customerId'])
            db = self._get_db()
            customer = db.read_customer(id)
            db.disconnect()

            if (customer == None):
                self._customerError.set_value('Customer {0} unknown'.format(id))
            else:
                self._customerId.set_value(customer.id)
                self._customerName.set_value(customer.name)
                self._customerStatus.set_value(self._translate_lov('status', title=customer.status))
                self._customerSegment.set_value(customer.segment)
                self._customerBirthNumber.set_value(customer.birth_no)
                self._customerRegistrationNumber.set_value(customer.reg_no)
                self._customerTaxNumber.set_value(customer.tax_no)
                self._customerError.set_value('')

    def _create_customer(self, data):
        """Method creates customer

        Args:
           data (dict): POST data

        Returns:
           none

        """
        
        if (data['customerName'] == ''):
            self._customerError.set_value('Name is mandatory')
        else:
            name = data['customerName']
            status = self._translate_lov('status', int(data['customerStatus']))
            segment = int(data['customerSegment'])
            birth_no = data['customerBirthNumber']
            reg_no = data['customerRegistrationNumber']
            tax_no = data['customerTaxNumber']

            db = self._get_db()
            id = db.create_customer(name, segment, status, birth_no, reg_no, tax_no)
            db.disconnect()
            
            if (id == None):
                self._customerError.set_value('Customer not created')
            else:
                self._customerId.set_value(id)
                self._customerName.set_value(name)
                self._customerStatus.set_value(int(data['customerStatus']))
                self._customerSegment.set_value(segment)
                self._customerBirthNumber.set_value(birth_no)
                self._customerRegistrationNumber.set_value(reg_no)
                self._customerTaxNumber.set_value(tax_no)
                self._customerError.set_value('')
        
    def _change_customer(self, data):
        """Method changes customer

        Args:
           data (dict): POST data

        Returns:
           none

        """
        
        if (data['customerId'] == ''):
            self._customerError.set_value('ID is mandatory')
        elif (data['customerName'] == ''):
            self._customerError.set_value('Name is mandatory')
        else:
            id = int(data['customerId'])
            name = data['customerName']
            status = self._translate_lov('status', int(data['customerStatus']))
            segment = int(data['customerSegment'])
            birth_no = data['customerBirthNumber']
            reg_no = data['customerRegistrationNumber']
            tax_no = data['customerTaxNumber']

            db = self._get_db()
            res = db.change_customer(id, name, status, segment, birth_no, reg_no, tax_no)
            db.disconnect()

            if (not res):
                self._customerError.set_value('Customer not changed')
            else:
                self._customerId.set_value(id)
                self._customerName.set_value(name)
                self._customerStatus.set_value(int(data['customerStatus']))
                self._customerSegment.set_value(segment)
                self._customerBirthNumber.set_value(birth_no)
                self._customerRegistrationNumber.set_value(reg_no)
                self._customerTaxNumber.set_value(tax_no)
                self._customerError.set_value('')

    def _read_payer(self, data):
        """Method reads payer

        Args:
           data (dict): POST data

        Returns:
           none

        """

        if (data['payerId'] == ''):
            self._payerError.set_value('ID is mandatory')
        else:
            id = int(data['payerId'])
            db = self._get_db()
            payer = db.read_payer(id)
            db.disconnect()

            if (payer == None):
                self._payerError.set_value('Payer {0} unknown'.format(id))
            else:
                self._payerId.set_value(payer.id)
                self._payerName.set_value(payer.name)
                self._payerStatus.set_value(self._translate_lov('status', title=payer.status))
                self._payerBillcycle.set_value(payer.billcycle)
                self._payerBankAccount.set_value(payer.bank_account)
                self._payerCustomer.set_value(payer.customer)
                self._payerError.set_value('')

    def _create_payer(self, data):
        """Method creates payer

        Args:
           data (dict): POST data

        Returns:
           none

        """

        if (data['payerName'] == ''):
            self._payerError.set_value('Name is mandatory')
        elif (data['payerCustomer'] == ''):
            self._payerError.set_value('Customer is mandatory')
        else:
            name = data['payerName']
            status = self._translate_lov('status', int(data['payerStatus']))
            billcycle = int(data['payerBillcycle'])
            bank_account = data['payerBankAccount']
            customer = data['payerCustomer']

            db = self._get_db()
            id = db.create_payer(name, billcycle, customer, status, bank_account)
            db.disconnect()

            if (id == None):
                self._payerError.set_value('Payer not created')
            else:
                self._payerId.set_value(id)
                self._payerName.set_value(name)
                self._payerStatus.set_value(int(data['payerStatus']))
                self._payerBillcycle.set_value(billcycle)
                self._payerBankAccount.set_value(bank_account)
                self._payerCustomer.set_value(customer)
                self._payerError.set_value('')

    def _change_payer(self, data):
        """Method changes payer

        Args:
           data (dict): POST data

        Returns:
           none

        """

        if (data['payerId'] == ''):
            self._payerError.set_value('ID is mandatory')
        elif (data['payerName'] == ''):
            self._payerError.set_value('Name is mandatory')
        elif (data['payerCustomer'] == ''):
            self._payerError.set_value('Customer is mandatory')
        else:
            id = int(data['payerId'])
            name = data['payerName']
            status = self._translate_lov('status', int(data['payerStatus']))
            billcycle = int(data['payerBillcycle'])
            bank_account = data['payerBankAccount']
            customer = int(data['payerCustomer'])

            db = self._get_db()
            res = db.change_payer(id, name, status, billcycle, bank_account, customer)
            db.disconnect()

            if (not res):
                self._payerError.set_value('Payer not changed')
            else:
                self._payerId.set_value(id)
                self._payerName.set_value(name)
                self._payerStatus.set_value(int(data['payerStatus']))
                self._payerBillcycle.set_value(billcycle)
                self._payerBankAccount.set_value(bank_account)
                self._payerCustomer.set_value(customer)
                self._payerError.set_value('')

    def _read_subscriber(self, data):
        """Method reads subscriber

        Args:
           data (dict): POST data

        Returns:
           none

        """

        if (data['subscriberId'] == ''):
            self._subscriberError.set_value('ID is mandatory')
        else:
            id = int(data['subscriberId'])
            db = self._get_db()
            subscriber = db.read_subscriber(id)
            db.disconnect()

            if (subscriber == None):
                self._subscriberError.set_value('Subscriber {0} unknown'.format(id))
            else:
                self._subscriberId.set_value(subscriber.id)
                self._subscriberName.set_value(subscriber.name)
                self._subscriberMsisdn.set_value(subscriber.msisdn)
                self._subscriberStatus.set_value(self._translate_lov('status', title=subscriber.status))
                self._subscriberMarket.set_value(subscriber.market)
                self._subscriberTariff.set_value(subscriber.tariff)
                self._subscriberCustomer.set_value(subscriber.customer)
                self._subscriberPayer.set_value(subscriber.payer)
                self._subscriberError.set_value('')

    def _create_subscriber(self, data):
        """Method creates subscriber

        Args:
           data (dict): POST data

        Returns:
           none

        """

        if (data['subscriberName'] == ''):
            self._subscriberError.set_value('Name is mandatory')
        elif (data['subscriberMsisdn'] == ''):
            self._subscriberError.set_value('MSISDN is mandatory')
        elif (data['subscriberCustomer'] == ''):
            self._subscriberError.set_value('Customer is mandatory')
        elif (data['subscriberPayer'] == ''):
            self._subscriberError.set_value('Payer is mandatory')
        else:
            name = data['subscriberName']
            msisdn = data['subscriberMsisdn']
            status = self._translate_lov('status', int(data['subscriberStatus']))
            market = int(data['subscriberMarket'])
            tariff = int(data['subscriberTariff'])
            customer = data['subscriberCustomer']
            payer = data['subscriberPayer']

            db = self._get_db()
            id = db.create_subscriber(name, msisdn, market, tariff, customer, payer, status)
            db.disconnect()

            if (id == None):
                self._subscriberError.set_value('Subscriber not created')
            else:
                self._subscriberId.set_value(id)
                self._subscriberName.set_value(name)
                self._subscriberMsisdn.set_value(msisdn)
                self._subscriberStatus.set_value(int(data['subscriberStatus']))
                self._subscriberMarket.set_value(market)
                self._subscriberTariff.set_value(tariff)
                self._subscriberCustomer.set_value(customer)
                self._subscriberPayer.set_value(payer)
                self._subscriberError.set_value('')

    def _change_subscriber(self, data):
        """Method changes subscriber

        Args:
           data (dict): POST data

        Returns:
           none

        """

        if (data['subscriberId'] == ''):
            self._subscriberError.set_value('ID is mandatory')
        elif (data['subscriberName'] == ''):
            self._subscriberError.set_value('Name is mandatory')
        elif (data['subscriberMsisdn'] == ''):
            self._subscriberError.set_value('MSISDN is mandatory')
        elif (data['subscriberCustomer'] == ''):
            self._subscriberError.set_value('Customer is mandatory')
        elif (data['subscriberPayer'] == ''):
            self._subscriberError.set_value('Payer is mandatory')
        else:
            id = int(data['subscriberId'])
            name = data['subscriberName']
            msisdn = data['subscriberMsisdn']
            status = self._translate_lov('status', int(data['subscriberStatus']))
            market = int(data['subscriberMarket'])
            tariff = int(data['subscriberTariff'])
            customer = int(data['subscriberCustomer'])
            payer = int(data['subscriberPayer'])

            db = self._get_db()
            res = db.change_subscriber(id, name, msisdn, status, market, tariff, customer, payer)
            db.disconnect()

            if (not res):
                self._subscriberError.set_value('Subscriber not changed')
            else:
                self._subscriberId.set_value(id)
                self._subscriberName.set_value(name)
                self._subscriberMsisdn.set_value(msisdn)
                self._subscriberStatus.set_value(int(data['subscriberStatus']))
                self._subscriberMarket.set_value(market)
                self._subscriberTariff.set_value(tariff)
                self._subscriberCustomer.set_value(customer)
                self._subscriberPayer.set_value(payer)
                self._subscriberError.set_value('')

    def _read_contact(self, data):
        """Method reads contact

        Args:
           data (dict): POST data

        Returns:
           none

        """

        if (data['contactId'] == ''):
            self._contactError.set_value('ID is mandatory')
        else:
            id = int(data['contactId'])
            db = self._get_db()
            contact = db.read_contact(id)
            db.disconnect()

            if (contact == None):
                self._contactError.set_value('Contact {0} unknown'.format(id))
            else:
                self._contactId.set_value(contact.id)
                self._contactName.set_value(contact.name)
                self._contactPhone.set_value(contact.phone)
                self._contactEmail.set_value(contact.email)
                self._contactError.set_value('')

                roles = []
                for role in contact.roles:
                    roles.append({'title': role.title, 'customer': role.customer,
                                  'payer': role.payer, 'subscriber': role.subscriber})
                self._contactRoleRoles = roles

    def _create_contact(self, data):
        """Method creates contact

        Args:
           data (dict): POST data

        Returns:
           none

        """

        if (data['contactName'] == ''):
            self._contactError.set_value('Name is mandatory')
        else:
            name = data['contactName']
            phone = data['contactPhone']
            email = data['contactEmail']

            db = self._get_db()
            id = db.create_contact(name, phone, email)
            db.disconnect()

            if (id == None):
                self._contactError.set_value('Contact not created')
            else:
                self._contactId.set_value(id)
                self._contactName.set_value(name)
                self._contactPhone.set_value(phone)
                self._contactEmail.set_value(email)
                self._contactError.set_value('')

    def _change_contact(self, data):
        """Method changes contact

        Args:
           data (dict): POST data

        Returns:
           none

        """

        if (data['contactId'] == ''):
            self._contactError.set_value('ID is mandatory')
        elif (data['contactName'] == ''):
            self._contactError.set_value('Name is mandatory')
        else:
            id = int(data['contactId'])
            name = data['contactName']
            phone = data['contactPhone']
            email = data['contactEmail']

            db = self._get_db()
            res = db.change_contact(id, name, phone, email)
            db.disconnect()

            if (not res):
                self._contactError.set_value('Contact not changed')
            else:
                self._contactId.set_value(id)
                self._contactName.set_value(name)
                self._contactPhone.set_value(phone)
                self._contactEmail.set_value(email)
                self._contactError.set_value('')

    def _assign_contact_role(self, data):
        """Method assigns contact role

        Args:
           data (dict): POST data

        Returns:
           none

        """

        if (data['contactId'] == ''):
            self._contactRoleError.set_value('Contact is mandatory')
        elif (data['contactRoleCustomer'] == '' and data['contactRolePayer'] == '' and data['contactRoleSubscriber'] == ''):
            self._contactRoleError.set_value('Customer or payer or subscriber is mandatory')
        else:
            id = int(data['contactId'])
            role = self._translate_lov('contact_role', int(data['contactRoleTitle']))
            customer = int(data['contactRoleCustomer']) if (data['contactRoleCustomer'] != '') else None
            payer = int(data['contactRolePayer']) if (data['contactRolePayer'] != '') else None
            subscriber = int(data['contactRoleSubscriber']) if (data['contactRoleSubscriber'] != '') else None

            db = self._get_db()
            res = db.assign_contact_role(id, role, customer, payer, subscriber)
            db.disconnect()

            if (not res):
                self._contactRoleError.set_value('Contact role not assigned')
            else:
                self._contactId.set_value(id)
                self._contactRoleTitle.set_value(int(data['contactRoleTitle']))
                self._contactRoleCustomer.set_value(customer)
                self._contactRolePayer.set_value(payer)
                self._contactRoleSubscriber.set_value(subscriber)
                self._contactRoleError.set_value('')
                self._contactRoleRoles.append({'title': role, 'customer': customer,
                                               'payer': payer, 'subscriber': subscriber})

    def _revoke_contact_role(self, data):
        """Method revokes contact role

        Args:
           data (dict): POST data

        Returns:
           none

        """

        if (data['contactId'] == ''):
            self._contactRoleError.set_value('Contact is mandatory')
        elif (data['contactRoleCustomer'] == '' and data['contactRolePayer'] == '' and data['contactRoleSubscriber'] == ''):
            self._contactRoleError.set_value('Customer or payer or subscriber is mandatory')
        else:
            id = int(data['contactId'])
            role = self._translate_lov('contact_role', int(data['contactRoleTitle']))
            customer = int(data['contactRoleCustomer']) if (data['contactRoleCustomer'] != '') else None
            payer = int(data['contactRolePayer']) if (data['contactRolePayer'] != '') else None
            subscriber = int(data['contactRoleSubscriber']) if (data['contactRoleSubscriber'] != '') else None

            db = self._get_db()
            res = db.revoke_contact_role(id, role, customer, payer, subscriber)
            db.disconnect()

            if (not res):
                self._contactRoleError.set_value('Contact role not revoked')
            else:
                self._contactId.set_value(id)
                self._contactRoleTitle.set_value(int(data['contactRoleTitle']))
                self._contactRoleCustomer.set_value(customer)
                self._contactRolePayer.set_value(payer)
                self._contactRoleSubscriber.set_value(subscriber)
                self._contactRoleError.set_value('')

                idx = 0
                for rec in self._contactRoleRoles:
                    if (rec['title'] == role):
                        if ((rec['customer'] != None and (rec['customer'] == customer)) or
                            (rec['payer'] != None and (rec['payer'] == payer)) or
                            (rec['subscriber'] != None and (rec['subscriber'] == subscriber))):
                            break
                    idx += 1
                del self._contactRoleRoles[idx]

    def _read_address(self, data):
        """Method reads address

        Args:
           data (dict): POST data

        Returns:
           none

        """

        if (data['addressId'] == ''):
            self._addressError.set_value('ID is mandatory')
        else:
            id = int(data['addressId'])
            db = self._get_db()
            address = db.read_address(id)
            db.disconnect()

            if (address == None):
                self._addressError.set_value('Address {0} unknown'.format(id))
            else:
                self._addressId.set_value(address.id)
                self._addressStreet.set_value(address.street)
                self._addressStreetNumber.set_value(address.street_no)
                self._addressCity.set_value(address.city)
                self._addressZip.set_value(address.zip)
                self._addressError.set_value('')

                roles = []
                for role in address.roles:
                    roles.append({'title': role.title, 'contact': role.contact, 'customer': role.customer,
                                  'payer': role.payer, 'subscriber': role.subscriber})
                self._addressRoleRoles = roles

    def _create_address(self, data):
        """Method creates address

        Args:
           data (dict): POST data

        Returns:
           none

        """

        if (data['addressStreet'] == ''):
            self._addressError.set_value('Street is mandatory')
        elif (data['addressStreetNumber'] == ''):
            self._addressError.set_value('Street number is mandatory')
        elif (data['addressCity'] == ''):
            self._addressError.set_value('City is mandatory')
        elif (data['addressZip'] == ''):
            self._addressError.set_value('ZIP is mandatory')
        else:
            street = data['addressStreet']
            street_no = data['addressStreetNumber']
            city = data['addressCity']
            czip = data['addressZip']

            db = self._get_db()
            id = db.create_address(street, street_no, city, czip)
            db.disconnect()

            if (id == None):
                self._addressError.set_value('Address not created')
            else:
                self._addressId.set_value(id)
                self._addressStreet.set_value(street)
                self._addressStreetNumber.set_value(street_no)
                self._addressCity.set_value(city)
                self._addressZip.set_value(czip)
                self._addressError.set_value('')

    def _change_address(self, data):
        """Method changes address

        Args:
           data (dict): POST data

        Returns:
           none

        """

        if (data['addressId'] == ''):
            self._addressError.set_value('ID is mandatory')
        elif (data['addressStreetNumber'] == ''):
            self._addressError.set_value('Street number is mandatory')
        elif (data['addressCity'] == ''):
            self._addressError.set_value('City is mandatory')
        elif (data['addressZip'] == ''):
            self._addressError.set_value('ZIP is mandatory')
        else:
            id = int(data['addressId'])
            street = data['addressStreet']
            street_no = data['addressStreetNumber']
            city = data['addressCity']
            zip = data['addressZip']

            db = self._get_db()
            res = db.change_address(id, street, street_no, city, zip)
            db.disconnect()

            if (not res):
                self._addressError.set_value('Address not changed')
            else:
                self._addressId.set_value(id)
                self._addressStreet.set_value(street)
                self._addressStreetNumber.set_value(street_no)
                self._addressCity.set_value(city)
                self._addressZip.set_value(zip)
                self._addressError.set_value('')

    def _assign_address_role(self, data):
        """Method assigns address role

        Args:
           data (dict): POST data

        Returns:
           none

        """

        if (data['addressId'] == ''):
            self._addressRoleError.set_value('Address is mandatory')
        elif (data['addressRoleContact'] == '' and data['addressRoleCustomer'] == ''
              and data['addressRolePayer'] == '' and data['addressRoleSubscriber'] == ''):
            self._contactRoleError.set_value('Contact or customer or payer or subscriber is mandatory')
        else:
            id = int(data['addressId'])
            role = self._translate_lov('address_role', int(data['addressRoleTitle']))
            contact = int(data['addressRoleContact']) if (data['addressRoleContact'] != '') else None
            customer = int(data['addressRoleCustomer']) if (data['addressRoleCustomer'] != '') else None
            payer = int(data['addressRolePayer']) if (data['addressRolePayer'] != '') else None
            subscriber = int(data['addressRoleSubscriber']) if (data['addressRoleSubscriber'] != '') else None

            db = self._get_db()
            res = db.assign_address_role(id, role, contact, customer, payer, subscriber)
            db.disconnect()

            if (not res):
                self._addressRoleError.set_value('Address role not assigned')
            else:
                self._addressId.set_value(id)
                self._addressRoleTitle.set_value(int(data['addressRoleTitle']))
                self._addressRoleContact.set_value(contact)
                self._addressRoleCustomer.set_value(customer)
                self._addressRolePayer.set_value(payer)
                self._addressRoleSubscriber.set_value(subscriber)
                self._addressRoleError.set_value('')
                self._addressRoleRoles.append({'title': role, 'contact': contact, 'customer': customer,
                                               'payer': payer, 'subscriber': subscriber})

    def _revoke_address_role(self, data):
        """Method revokes address role

        Args:
           data (dict): POST data

        Returns:
           none

        """

        if (data['addressId'] == ''):
            self._addressRoleError.set_value('Address is mandatory')
        elif (data['addressRoleContact'] == '' and data['addressRoleCustomer'] == '' and
              data['addressRolePayer'] == '' and data['addressRoleSubscriber'] == ''):
            self._addressRoleError.set_value('Contact or customer or payer or subscriber is mandatory')
        else:
            id = int(data['addressId'])
            role = self._translate_lov('address_role', int(data['addressRoleTitle']))
            contact = int(data['addressRoleContact']) if (data['addressRoleContact'] != '') else None
            customer = int(data['addressRoleCustomer']) if (data['addressRoleCustomer'] != '') else None
            payer = int(data['addressRolePayer']) if (data['addressRolePayer'] != '') else None
            subscriber = int(data['addressRoleSubscriber']) if (data['addressRoleSubscriber'] != '') else None

            db = self._get_db()
            res = db.revoke_address_role(id, role, contact, customer, payer, subscriber)
            db.disconnect()

            if (not res):
                self._addressRoleError.set_value('Address role not revoked')
            else:
                self._addressId.set_value(id)
                self._addressRoleTitle.set_value(int(data['addressRoleTitle']))
                self._addressRoleContact.set_value(contact)
                self._addressRoleCustomer.set_value(customer)
                self._addressRolePayer.set_value(payer)
                self._addressRoleSubscriber.set_value(subscriber)
                self._addressRoleError.set_value('')

                idx = 0
                for rec in self._addressRoleRoles:
                    if (rec['title'] == role):
                        if ((rec['contact'] != None and (rec['contact'] == contact)) or
                            (rec['customer'] != None and (rec['customer'] == customer)) or
                            (rec['payer'] != None and (rec['payer'] == payer)) or
                            (rec['subscriber'] != None and (rec['subscriber'] == subscriber))):
                            break
                    idx += 1
                del self._addressRoleRoles[idx]
