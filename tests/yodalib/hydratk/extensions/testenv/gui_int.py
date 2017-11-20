# -*- coding: utf-8 -*-
"""GUI interface methods to be used in helpers

.. module:: yodalib.testenv.gui_int
   :platform: Unix
   :synopsis: GUI interface methods
.. moduleauthor:: Petr Rašek <bowman@hydratk.org>

"""

from hydratk.core.masterhead import MasterHead
from hydratk.lib.bridge.selen import SeleniumBridge
from hydratk.extensions.testenv.entities import Customer, Payer, Subscriber, Contact, ContactRole, Address, AddressRole

class GUI_INT(object):

    _mh = None
    _url = None
    _client = None

    def __init__(self, browser='Firefox'):
        """Class constructor

        Called when the object is initialized

        Args:
           browser (str): browser

        """

        self._mh = MasterHead.get_head()
        ip = self._mh.cfg['Extensions']['TestEnv']['server_ip']
        port = self._mh.cfg['Extensions']['TestEnv']['server_port']
        self._url = 'http://{0}:{1}'.format(ip, port)
        self._client = SeleniumBridge(browser)

    def open(self):
        """Method opens browser

        Args:
           none

        Returns:
           bool

        """

        res = self._client.open(self._url)
        self._client.wait_for_element('customerId')

        return res

    def close(self):
        """Method closes browser

        Args:
           none

        Returns:
           bool

        """

        return self._client.close()

    def switch_tab(self, id):
        """Method switches tab

        Args:
           id (str): tab id

        Returns:
           none

        """

        self._client.set_element(id, el_type='submit')

    def read_customer(self, id):
        """Method reads customer

        Args:
           id (int): customer id

        Returns:
           obj: entities.Customer

        """

        self._client.set_element('customerId', id)
        self._client.set_element('customerRead', el_type='submit')

        if (self._client.read_element('customerError') != ''):
            return None
        else:
            customer = Customer(self._client.read_element('customerId'),
                                self._client.read_element('customerName'),
                                self._client.read_element('customerStatus', el_type='select'),
                                self._client.read_element('customerSegment', el_type='select'),
                                self._client.read_element('customerBirthNumber'),
                                self._client.read_element('customerRegistrationNumber'),
                                self._client.read_element('customerTaxNumber'))
            return customer

    def create_customer(self, name, status, segment, birth_no=None, reg_no=None, tax_no=None):
        """Method creates customer

        Args:
           name (str): name
           status (str): status, lov_status.title
           segment (int): segment id, lov_segment.id
           birth_no (str): birth number
           reg_no (str): registration number
           tax_no (str): tax identification number

        Returns:
           int: created customer id

        """

        self._client.set_element('customerName', name)
        self._client.set_element('customerStatus', status, el_type='select')
        self._client.set_element('customerSegment', segment, el_type='select')
        if (birth_no != None):
            self._client.set_element('customerBirthNumber', birth_no)
        if (reg_no != None):
            self._client.set_element('customerRegistrationNumber', reg_no)
        if (tax_no != None):
            self._client.set_element('customerTaxNumber', tax_no)
        self._client.set_element('customerCreate', el_type='submit')

        if (self._client.read_element('customerError') != ''):
            return None
        else:
            return self._client.read_element('customerId')

    def change_customer(self, id, name=None, status=None, segment=None, birth_no=None, reg_no=None, tax_no=None):
        """Method changes customer

        Args:
           id (int): customer id
           name (str): name
           status (str): status, lov_status.title
           segment (int): segment id, lov_segment.id
           birth_no (str): birth number
           reg_no (str): registration number
           tax_no (str): tax identification number

        Returns:
           bool: result

        """

        self._client.set_element('customerId', id)
        if (name != None):
            self._client.set_element('customerName', name)
        if (status != None):
            self._client.set_element('customerStatus', status, el_type='select')
        if (segment != None):
            self._client.set_element('customerSegment', segment, el_type='select')
        if (birth_no != None):
            self._client.set_element('customerBirthNumber', birth_no)
        if (reg_no != None):
            self._client.set_element('customerRegistrationNumber', reg_no)
        if (tax_no != None):
            self._client.set_element('customerTaxNumber', tax_no)
        self._client.set_element('customerChange', el_type='submit')

        if (self._client.read_element('customerError') != ''):
            return False
        else:
            return True

    def read_payer(self, id):
        """Method reads payer

        Args:
           id (int): payer id

        Returns:
           obj: entities.Payer

        """

        self._client.set_element('payerId', id)
        self._client.set_element('payerRead', el_type='submit')

        if (self._client.read_element('payerError') != ''):
            return None
        else:
            payer = Payer(self._client.read_element('payerId'),
                          self._client.read_element('payerName'),
                          self._client.read_element('payerStatus', el_type='select'),
                          self._client.read_element('payerBillcycle', el_type='select'),
                          self._client.read_element('payerCustomer'),
                          self._client.read_element('payerBankAccount'))
            return payer

    def create_payer(self, name, status, billcycle, customer, bank_account=None):
        """Method creates payer

        Args:
           name (str): name
           status (str): status, lov_status.title
           billcycle (int): billcycle, lov_billcycle.id
           customer (int): assigned customer id
           bank_account (str): banking account

        Returns:
           int: created payer id

        """

        self._client.set_element('payerName', name)
        self._client.set_element('payerStatus', status, el_type='select')
        self._client.set_element('payerBillcycle', billcycle, el_type='select')
        if (bank_account != None):
            self._client.set_element('payerBankAccount', bank_account)
        self._client.set_element('payerCustomer', customer)
        self._client.set_element('payerCreate', el_type='submit')

        if (self._client.read_element('payerError') != ''):
            return None
        else:
            return self._client.read_element('payerId')

    def change_payer(self, id, name=None, status=None, billcycle=None, bank_account=None, customer=None):
        """Method changes payer

        Args:
           id (int): payer id
           name (str): name
           status (str): status, lov_status.title
           billcycle (int): billcycle id, lov_billcycle.id
           bank_account (str): banking account
           customer (int): assigned customer id

        Returns:
           bool: result

        """

        self._client.set_element('payerId', id)
        if (name != None):
            self._client.set_element('payerName', name)
        if (status != None):
            self._client.set_element('payerStatus', status, el_type='select')
        if (billcycle != None):
            self._client.set_element('payerBillcycle', billcycle, el_type='select')
        if (bank_account != None):
            self._client.set_element('payerBankAccount', bank_account)
        if (customer != None):
            self._client.set_element('payerCustomer', customer)
        self._client.set_element('payerChange', el_type='submit')

        if (self._client.read_element('payerError') != ''):
            return False
        else:
            return True

    def read_subscriber(self, id):
        """Method reads subscriber

        Args:
           id (int): subscriber id

        Returns:
           obj: entities.Subscriber

        """

        self._client.set_element('subscriberId', id)
        self._client.set_element('subscriberRead', el_type='submit')

        if (self._client.get_element('subscriberError').get_attribute('value') != ''):
            return None
        else:
            subscriber = Subscriber(self._client.read_element('subscriberId'),
                                    self._client.read_element('subscriberName'),
                                    self._client.read_element('subscriberMsisdn'),
                                    self._client.read_element('subscriberStatus', el_type='select'),
                                    self._client.read_element('subscriberMarket', el_type='select'),
                                    self._client.read_element('subscriberTariff', el_type='select'),
                                    self._client.read_element('subscriberCustomer'),
                                    self._client.read_element('subscriberPayer'))
            return subscriber

    def create_subscriber(self, name, msisdn, status, market, tariff, customer, payer):
        """Method creates subscriber

        Args:
           name (str): name
           msisdn (str): MSISDN
           status (str): status, lov_status.title
           market (int): market id, lov_market.id
           tariff (int): tariff id, lov_tariff.id
           customer (int): assigned customer id
           payer (int): assigned payer id

        Returns:
           int: created subscriber id

        """

        self._client.set_element('subscriberName', name)
        self._client.set_element('subscriberMsisdn', msisdn)
        self._client.set_element('subscriberStatus', status, el_type='select')
        self._client.set_element('subscriberMarket', market, el_type='select')
        self._client.set_element('subscriberTariff', tariff, el_type='select')
        self._client.set_element('subscriberCustomer', customer)
        self._client.set_element('subscriberPayer', payer)
        self._client.set_element('subscriberCreate', el_type='submit')

        if (self._client.read_element('subscriberError') != ''):
            return None
        else:
            return self._client.read_element('subscriberId')

    def change_subscriber(self, id, name=None, msisdn=None, status=None, market=None, tariff=None, customer=None, payer=None):
        """Method changes subscriber

        Args:
           id (int): subscriber id
           name (str): name
           msisdn (str): MSISDN
           status (str): status, lov_status.title
           market (int): market id, lov_market.id
           tariff (int): tariff id, lov_tariff.id
           customer (int): assigned customer id
           payer (int): assigned payer id

        Returns:
           result: bool

        """

        self._client.set_element('subscriberId', id)
        if (name != None):
            self._client.set_element('subscriberName', name)
        if (msisdn != None):
            self._client.set_element('subscriberMsisdn', msisdn)
        if (status != None):
            self._client.set_element('subscriberStatus', status, el_type='select')
        if (market != None):
            self._client.set_element('subscriberMarket', market, el_type='select')
        if (tariff != None):
            self._client.set_element('subscriberTariff', tariff, el_type='select')
        if (customer != None):
            self._client.set_element('subscriberCustomer', customer)
        if (payer != None):
            self._client.set_element('subscriberPayer', payer)
        self._client.set_element('subscriberChange', el_type='submit')

        if (self._client.read_element('subscriberError') != ''):
            return False
        else:
            return True

    def read_contact(self, id):
        """Method reads contact

        Args:
           id (int): contact id

        Returns:
           obj: entities.Contact

        """

        self._client.set_element('contactId', id)
        self._client.set_element('contactRead', el_type='submit')

        if (self._client.read_element('contactError') != ''):
            return None
        else:
            table = self._client.get_element('contactRoles').find_element_by_tag_name('tbody')

            roles = []
            for row in table.find_elements_by_tag_name('tr'):
                cols = row.find_elements_by_tag_name('td')
                title = cols[0].text
                customer = cols[1].text if len(cols[1].text) > 0 else None
                payer = cols[2].text if len(cols[2].text) > 0 else None
                subscriber = cols[3].text if len(cols[3].text) > 0 else None
                roles.append(ContactRole(id, title, customer, payer, subscriber))

            contact = Contact(self._client.read_element('contactId'),
                              self._client.read_element('contactName'),
                              self._client.read_element('contactPhone'),
                              self._client.read_element('contactEmail'),
                              roles)
            return contact

    def create_contact(self, name, phone=None, email=None):
        """Method creates contact

        Args:
           name (str): name
           phone (str): phone number
           email (str): email

        Returns:
           int: created contact id

        """

        self._client.set_element('contactName', name)
        if (phone != None):
            self._client.set_element('contactPhone', phone)
        if(email != None):
            self._client.set_element('contactEmail', email)
        self._client.set_element('contactCreate', el_type='submit')

        if (self._client.read_element('contactError') != ''):
            return None
        else:
            return self._client.read_element('contactId')

    def change_contact(self, id, name=None, phone=None, email=None):
        """Method changes contact

        Args:
           id (int): contact id
           name (str): name
           phone (str): phone number
           email (str): email

        Returns:
           bool: result

        """

        self._client.set_element('contactId', id)
        if (name != None):
            self._client.set_element('contactName', name)
        if (phone != None):
            self._client.set_element('contactPhone', phone)
        if (email != None):
            self._client.set_element('contactEmail', email)
        self._client.set_element('contactChange', el_type='submit')

        if (self._client.read_element('contactError') != ''):
            return False
        else:
            return True

    def assign_contact_role(self, id, title, customer='', payer='', subscriber=''):
        """Method assigns contact role

        Args:
           id (int): contact id
           role (str): role title, lov_contact_role.title
           customer (int): assigned customer id
           payer (int): assigned payer id
           subscriber (int): assigned subscriber id

        Returns:
           bool: result

        """

        self._client.set_element('contactId', id)
        self._client.set_element('contactRoleTitle', title, el_type='select')
        self._client.set_element('contactRoleCustomer', customer)
        self._client.set_element('contactRolePayer', payer)
        self._client.set_element('contactRoleSubscriber', subscriber)
        self._client.set_element('contactRoleAssign', el_type='submit')

        return True

    def revoke_contact_role(self, id, title, customer='', payer='', subscriber=''):
        """Method assigns contact role

        Args:
           id (int): contact id
           role (str): role title, lov_contact_role.title
           customer (int): assigned customer id
           payer (int): assigned payer id
           subscriber (int): assigned subscriber id

        Returns:
           bool: result

        """

        self._client.set_element('contactId', id)
        self._client.set_element('contactRoleTitle', title, el_type='select')
        self._client.set_element('contactRoleCustomer', customer)
        self._client.set_element('contactRolePayer', payer)
        self._client.set_element('contactRoleSubscriber', subscriber)
        self._client.set_element('contactRoleRevoke', el_type='submit')

        return True

    def read_address(self, id):
        """Method reads address

        Args:
           id (int): address id

        Returns:
           obj: entities.Address

        """

        self._client.set_element('addressId', id)
        self._client.set_element('addressRead', el_type='submit')

        if (self._client.read_element('addressError') != ''):
            return None
        else:
            table = self._client.get_element('addressRoles').find_element_by_tag_name('tbody')

            roles = []
            for row in table.find_elements_by_tag_name('tr'):
                cols = row.find_elements_by_tag_name('td')
                title = cols[0].text
                contact = cols[1].text if len(cols[1].text) > 0 else None
                customer = cols[2].text if len(cols[2].text) > 0 else None
                payer = cols[3].text if len(cols[3].text) > 0 else None
                subscriber = cols[4].text if len(cols[4].text) > 0 else None
                roles.append(AddressRole(id, title, contact, customer, payer, subscriber))
            address = Address(self._client.read_element('addressId'),
                              self._client.read_element('addressStreet'),
                              self._client.read_element('addressStreetNumber'),
                              self._client.read_element('addressCity'),
                              self._client.read_element('addressZip'),
                              roles)
            return address

    def create_address(self, street, street_no, city, zip):
        """Method creates address

        Args:
           street (str): street
           street_no (str): street number
           city (str): city
           zip (int): zip code

        Returns:
           int: created address id

        """

        self._client.set_element('addressStreet', street)
        self._client.set_element('addressStreetNumber', street_no)
        self._client.set_element('addressCity', city)
        self._client.set_element('addressZip', zip)
        self._client.set_element('addressCreate', el_type='submit')

        if (self._client.read_element('addressError') != ''):
            return None
        else:
            return self._client.read_element('addressId')

    def change_address(self, id, street=None, street_no=None, city=None, zip=None):
        """Method changes address

        Args:
           id (int): address id
           street (str): street
           street_no (str): street number
           city (str): city
           zip (int): zip code

        Returns:
           bool: result

        """

        self._client.set_element('addressId', id)
        if (street != None):
            self._client.set_element('addressStreet', street)
        if (street_no != None):
            self._client.set_element('addressStreetNumber', street_no)
        if (city != None):
            self._client.set_element('addressCity', city)
        if (zip != None):
            self._client.set_element('addressZip', zip)
        self._client.set_element('addressChange', el_type='submit')

        if (self._client.read_element('addressError') != ''):
            return False
        else:
            return True

    def assign_address_role(self, id, title, contact='', customer='', payer='', subscriber=''):
        """Method assigns address role

        Args:
           id (int): contact id
           role (str): role title, lov_address_role.title
           contact (int): assigned contact id
           customer (int): assigned customer id
           payer (int): assigned payer id
           subscriber (int): assigned subscriber id

        Returns:
           bool: result

        """

        self._client.set_element('addressId', id)
        self._client.set_element('addressRoleTitle', title, el_type='select')
        self._client.set_element('addressRoleContact', contact)
        self._client.set_element('addressRoleCustomer', customer)
        self._client.set_element('addressRolePayer', payer)
        self._client.set_element('addressRoleSubscriber', subscriber)
        self._client.set_element('addressRoleAssign', el_type='submit')

        return True

    def revoke_address_role(self, id, title, contact='', customer='', payer='', subscriber=''):
        """Method revokes address role

        Args:
           id (int): contact id
           role (str): role title, lov_address_role.title
           contact (int): assigned contact id
           customer (int): assigned customer id
           payer (int): assigned payer id
           subscriber (int): assigned subscriber id

        Returns:
           bool: result

        """

        self._client.set_element('addressId', id)
        self._client.set_element('addressRoleTitle', title, el_type='select')
        self._client.set_element('addressRoleContact', contact)
        self._client.set_element('addressRoleCustomer', customer)
        self._client.set_element('addressRolePayer', payer)
        self._client.set_element('addressRoleSubscriber', subscriber)
        self._client.set_element('addressRoleRevoke', el_type='submit')

        return True
