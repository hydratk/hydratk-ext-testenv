# -*- coding: utf-8 -*-
"""Web server

.. module:: testenv.web_server
   :platform: Unix
   :synopsis: Web server
.. moduleauthor:: Petr Rašek <bowman@hydratk.org>

"""

from hydratk.core.masterhead import MasterHead
from hydratk.extensions.testenv.rest_handler import RestHandler
from hydratk.extensions.testenv.soap_handler import SoapHandler
from hydratk.extensions.testenv.gui_handler import GuiHandler
import hydratk.lib.system.config as syscfg
from web import application, httpserver, input, data, NotFound, header, ctx
from os import path

urls = (
    '/', 'Index',
    '/rs/customer', 'Customer',
    '/rs/payer', 'Payer',
    '/rs/subscriber', 'Subscriber',
    '/rs/contact', 'Contact',
    '/rs/contact/role', 'ContactRole',
    '/rs/address', 'Address',
    '/rs/address/role', 'AddressRole',
    '/rs/service', 'Service',
    '/ws/crm', 'SoapService'
)

mh = None
gui = None
rest = None
soap = None

class Server(object):
    """Class Server
    """

    _server = None

    def __init__(self):
        """Class constructor

        Called when the object is initialized    

        Args:
           none

        """

        global mh
        global gui
        global rest
        global soap

        mh = MasterHead.get_head()
        gui = GuiHandler()
        rest = RestHandler()
        soap = SoapHandler()

    def _start(self):
        """Method starts web server   

        Args:
           none

        Returns:
           void       

        """

        ip = mh.cfg['Extensions']['TestEnv']['server_ip']
        port = mh.cfg['Extensions']['TestEnv']['server_port']
        self._server = application(urls, globals())
        httpserver.runsimple(self._server.wsgifunc(), (str(ip), port))


class Index(object):
    """Handles requests on /
    """

    def GET(self):

        return gui.render_page()
    
    def POST(self):
        
        return gui.render_page(input())


class Customer(object):
    """Handles requests on /rs/customer                           
    """

    def GET(self):

        return rest.read_customer(input())

    def POST(self):

        return rest.create_customer(data())

    def PUT(self):

        return rest.change_customer(data())


class Payer(object):
    """Handles requests on /rs/payer                           
    """

    def GET(self):

        return rest.read_payer(input())

    def POST(self):

        return rest.create_payer(data())

    def PUT(self):

        return rest.change_payer(data())


class Subscriber(object):
    """Handles requests on /rs/subscriber                           
    """

    def GET(self):

        return rest.read_subscriber(input())

    def POST(self):

        return rest.create_subscriber(data())

    def PUT(self):

        return rest.change_subscriber(data())


class Contact(object):
    """Handles requests on /rs/contact                           
    """

    def GET(self):

        return rest.read_contact(input())

    def POST(self):

        return rest.create_contact(data())

    def PUT(self):

        return rest.change_contact(data())


class ContactRole(object):
    """Handles requests on /rs/contact/role                           
    """

    def POST(self):

        return rest.assign_contact_role(data())

    def PUT(self):

        return rest.revoke_contact_role(data())


class Address(object):
    """Handles requests on /rs/address                           
    """

    def GET(self):

        return rest.read_address(input())

    def POST(self):

        return rest.create_address(data())

    def PUT(self):

        return rest.change_address(data())


class AddressRole(object):
    """Handles requests on /rs/address/role                           
    """

    def POST(self):

        return rest.assign_address_role(data())

    def PUT(self):

        return rest.revoke_address_role(data())


class Service(object):
    """Handles requests on /rs/service                           
    """

    def GET(self):

        return rest.read_services(input())

    def POST(self):

        return rest.create_service(data())

    def PUT(self):

        return rest.change_service(data())


class SoapService(object):
    """Handles requests on /ws/crm                           
    """

    def GET(self):

        key = list(input().keys())[0]
        ext_dir = mh.cfg['Extensions']['TestEnv']['ext_dir'].format(var_dir=syscfg.HTK_VAR_DIR)

        if (key == 'wsdl'):
            soap_file = path.join(ext_dir, 'crm.wsdl')
        elif (key == 'xsd'):
            soap_file = path.join(ext_dir, 'crm.xsd')
        else:
            return NotFound()

        if (path.exists(soap_file)):
            with open(soap_file, 'r') as file:
                header('Content-Type', 'text/xml')
                return file.read()
        else:
            mh.dmsg('htk_on_extension_error', self._mh._trn.msg('te_web_unknown_file', soap_file),
                    self._mh.fromhere())
            return NotFound()

    def POST(self):

        return soap.dispatcher(ctx.env, data())
