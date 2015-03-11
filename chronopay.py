#!/usr/bin/env python2

import logging
from suds.client import Client


logging.basicConfig(level=logging.INFO)
logging.getLogger('suds.client').setLevel(logging.DEBUG)

url = 'file:/home/itari/djcode/soap/api3.wsdl'

client = Client(url, cache=None)
login = 'choronopay'
password = 'choronopay'
login_res = client.service.Login(login, password)

result = client.service.getAgreements(agrmid=1410)
print result