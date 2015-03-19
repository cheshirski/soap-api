#!/usr/bin/env python2
# coding: utf-8

import logging
from datetime import datetime
from suds.client import Client


# Словарь ответов статусов от soapPayment
status_payment = {
    '0': 'Платеж проведен',
    '2': 'Платеж анулирован',
}

logging.basicConfig(level=logging.INFO)
logging.getLogger('suds.client').setLevel(logging.DEBUG)

url = 'file:/home/itari/djcode/soap/api3.wsdl'

client = Client(url, cache=None)
login = 'choronopay'
password = 'choronopay'

timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# Осуществляем подключение к биллингу
login_res = client.service.Login(login, password)

soap_payment = client.factory.create('soapPayment')
soap_payment.modperson = 0        # идентификатор менеджера проводившего платеж
soap_payment.currid = 0           # Идентификатор валюты платежа
soap_payment.amount = 10          # сумма платежа
soap_payment.paydate = str(timestamp)     # дата платежа
soap_payment.receipt = 131549657  # идентификатор платежа(В моем случае это transaction_id)
soap_payment.comment = 'TEST'       # тут и ежу понятно
soap_payment.classid = 0          # идентификатор категории платежа

result = client.service.ExternPayment(11, 779, 0, soap_payment, notexists=1)

client.service.Logout()