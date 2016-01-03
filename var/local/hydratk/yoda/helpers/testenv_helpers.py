# -*- coding: utf-8 -*-
"""This code is part of TestEnv extension

.. module:: testenv.helpers
   :platform: Unix
   :synopsis: TestEnv helpers
.. moduleauthor:: Petr Rašek <bowman@hydratk.org>

"""

from hydratk.extensions.testenv.entities.crm_entities import Customer, Payer, Subscriber;
from hydratk.extensions.testenv.entities.crm_entities import Contact, ContactRole, Address, AddressRole;
from hydratk.extensions.testenv.entities.crm_entities import Service, ServiceOperation;
from hydratk.extensions.testenv.interfaces.db_int import DB_INT as db;
from hydratk.extensions.testenv.interfaces.rest_int import REST_INT as rest;
from hydratk.extensions.testenv.interfaces.soap_int import SOAP_INT as soap;