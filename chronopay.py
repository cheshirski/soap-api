#!/usr/bin/env python2
# coding: utf-8

import logging
import cgi
from datetime import datetime
from time import localtime, strftime
from suds.client import Client

# Включено для логирования
import cgitb

cgitb.enable()

# Словарь ответов статусов от soapPayment
status_payment = {
    '0': 'Платеж проведен',
    '2': 'Платеж анулирован',
}

logging.basicConfig(level=logging.INFO)
logging.getLogger('suds.client').setLevel(logging.DEBUG)

print "Content-Type: text/plain;charset=utf-8"
print ""

f = open('/tmp/chronopay.log', 'a')

form = cgi.FieldStorage()
f.write("----------------- current date transaction %s -----------------\n" % strftime("%a, %d %b %Y %H:%M:%S", localtime()))
for key in form.keys():
    f.write("%s = %s\n" % (key, form[key].value))

url = 'file:/home/itari/djcode/soap/api3.wsdl'

client = Client(url, cache=None)
login = 'choronopay'
password = 'choronopay'

timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
agrmid = str(form['cs1'].value)

# Осуществляем подключение к биллингу
login_res = client.service.Login(login, password)

soap_payment = client.factory.create('soapPayment')
soap_payment.modperson = 0  # идентификатор менеджера проводившего платеж
soap_payment.currid = 0  # Идентификатор валюты платежа
soap_payment.amount = str(form['total'].value)  # сумма платежа
soap_payment.paydate = str(timestamp)  # дата платежа
soap_payment.receipt = str(form['transaction_id'].value)  # идентификатор платежа(В моем случае это transaction_id)
# soap_payment.comment = 'TEST'  # тут и ежу понятно
soap_payment.classid = 0  # идентификатор категории платежа

result = client.service.ExternPayment(11, agrmid, 0, soap_payment, notexists=1)

client.service.Logout()
