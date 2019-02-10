#-*- coding: utf-8 -*-
__author__ = 'rdk'

from flask import render_template, flash, request, redirect
from flask_weasyprint import HTML, render_pdf
from app import app, db
from app.models import Invoice, Presta

class GenericObject(object):
    pass

@app.route('/invoice')
def invoice():
    invoices = Invoice.query.order_by(Invoice.number).all()
    return render_template('invoice_overview.html', invoices=invoices)

@app.route('/invoice/view/<iid>')
def get_invoice(iid):
    invoice = Invoice.query.filter(Invoice.id == iid).first()
    p = Presta.query \
        .filter(Presta.invoice_number == invoice.number) \
        .order_by(Presta.date).all()

    lst_presta = []
    presta_range = GenericObject()
    invoice_data = GenericObject()
    price = GenericObject()
    notification = GenericObject()
    bank = GenericObject()

    for i in p:
        presta = GenericObject()
        presta.project = i.project.code
        presta.date = i.date
        presta.description = i.description
        presta.hours = ("%.2f" % (i.duration / 3600.0))

        lst_presta.append(presta)

    invoice_data.date = invoice.date.strftime('%d/%m/%Y')
    invoice_data.number = invoice.number
    bank.account = invoice.bank_account
    bank.swift = invoice.bank_swift

    if invoice.notification is not None:
        notification.text = invoice.notification.notification
    else:
        notification = None

    presta_range.from_date = lst_presta[0].date.strftime('%d/%m/%Y')
    presta_range.to_date = lst_presta[len(lst_presta) - 1].date.strftime('%d/%m/%Y')
    presta_range.total_days = round(invoice.work_days, 2)

    price.htva = round(invoice.price_htva, 2)
    price.tva = round(invoice.price_total - invoice.price_htva, 2)
    price.total = round(invoice.price_total, 2)

    html = render_template('timesheet.html', customer=invoice.customer, invoice=invoice_data, presta_range=presta_range,
                           prestas=lst_presta, price=price, notification=notification, bank=bank)

    return render_pdf(HTML(string=html))