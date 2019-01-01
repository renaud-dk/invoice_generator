#-*- coding: utf-8 -*-
__author__ = 'rdk'

import os
from datetime import timedelta, datetime
from flask import render_template, flash, redirect, request
from flask_weasyprint import HTML, render_pdf
from werkzeug.utils import secure_filename
from app import app, db, FILE_TYPE_PST, FILE_TYPE_PRJ, REF_INVOICE_NUMBER, REF_BANK_ACCOUNT, REF_BANK_SWIFT
from app import REPORT_TYPE_HOLIDAYS, REPORT_TYPE_TRAVELS, REPORT_TYPE_PRESTAS
from app.models import Customer, Project, Presta, Refvalue, Invoice, Notification
from app.forms import InvoiceForm, UploadForm, ReportForm
from app.utils import import_to_db


class GenericObject(object):
    pass


class select_type(object):
    def __init__(self, identifier, description):
        self.identifier = identifier
        self.description = description


upload_file_types = [select_type(FILE_TYPE_PRJ, "Project Export"),
                     select_type(FILE_TYPE_PST, "Presta Export")]

report_types = [select_type(REPORT_TYPE_HOLIDAYS, "Off days"),
                select_type(REPORT_TYPE_TRAVELS, "Travels"),
                select_type(REPORT_TYPE_PRESTAS, "Prestas")]

@app.route('/admin/gen_invoice', methods=['GET', 'POST'])
def gen_invoice():
    invoicefrm = InvoiceForm()
    invoicefrm.customer.choices = [(c.id, c.name) for c in Customer.query.all()]

    if invoicefrm.validate_on_submit():
        from_date = datetime.strptime(invoicefrm.date_from.data, '%d/%m/%Y')
        to_date = datetime.strptime(invoicefrm.date_to.data, '%d/%m/%Y')

        p = Presta.query.join(Project) \
            .join(Customer) \
            .filter(Customer.id == invoicefrm.customer.data) \
            .filter(Project.code != 'Off') \
            .filter(Presta.date >= from_date) \
            .filter(Presta.date <= (to_date + timedelta(days=1))) \
            .order_by(Presta.date).all()

        # p = Presta.query.all()
        lst_presta = []
        presta_range = GenericObject()
        invoice = GenericObject()
        price = GenericObject()
        daily_rate = float(Customer.query.filter(Customer.id == invoicefrm.customer.data).first().rate)
        work_days = 0

        for i in p:
            presta = GenericObject()
            presta.project = i.project.code
            presta.date = i.date
            presta.description = i.description
            presta.hours = ("%.2f" % (i.duration / 3600.0))

            lst_presta.append(presta)
            work_days += i.duration

        work_days = (work_days / 3600.0) / 8.0
        customer = p[0].project.customer
        invoice.date = to_date.strftime('%d/%m/%Y')
        invoice.number = Refvalue.query.filter(Refvalue.refname == REF_INVOICE_NUMBER).first().refvalue
        presta_range.from_date = lst_presta[0].date.strftime('%d/%m/%Y')
        presta_range.to_date = lst_presta[len(lst_presta) - 1].date.strftime('%d/%m/%Y')
        presta_range.total_days = round(work_days, 2)
        price.htva = round(daily_rate * work_days, 2)
        price.tva = round(price.htva * 0.21, 2)
        price.total = price.htva + price.tva

        dt = datetime.now()

        notif = Notification.query \
            .filter(dt >= Notification.date_from) \
            .filter(dt <= Notification.date_to).first()

        if notif is not None:
            notification = GenericObject()
            notification.text = notif.notification
        else:
            notification = None

        bank = GenericObject()
        bank.account = Refvalue.query.filter(Refvalue.refname == REF_BANK_ACCOUNT).first().refvalue
        bank.swift = Refvalue.query.filter(Refvalue.refname == REF_BANK_SWIFT).first().refvalue

        html = render_template('timesheet.html', customer=customer, invoice=invoice, presta_range=presta_range,
                               prestas=lst_presta, price=price, notification=notification, bank=bank)

        if invoicefrm.is_official.data == True:
            invoice_number = Refvalue.query.filter(Refvalue.refname == REF_INVOICE_NUMBER).first()

            # udpate prestat with invoice number 
            for i in p:
                i.invoice_number = invoice_number.refvalue
                db.session.add(i)

            # increment invoice_number
            invoice_number.refvalue = str(int(invoice_number.refvalue) + 1)
            db.session.add(invoice_number)

            new_invoice_hist = Invoice()
            new_invoice_hist.number = invoice.number
            new_invoice_hist.date = to_date
            new_invoice_hist.work_days = work_days
            new_invoice_hist.price_htva = price.htva
            new_invoice_hist.price_total = price.total
            new_invoice_hist.daily_rate = daily_rate
            new_invoice_hist.customer_id = invoicefrm.customer.data

            db.session.add(new_invoice_hist)

            db.session.commit()

        return render_pdf(HTML(string=html))

    return render_template('overview.html', invoice=invoicefrm)

@app.route('/admin/gen_report', methods = ['GET', 'POST'])
def gen_report():
    reporfrm = ReportForm()
    reporfrm.report_type.choices = [(r.identifier, r.description) for r in report_types]
    customers = Customer.query.all()
    reporfrm.customer.choices = [("%", "All")]
    reporfrm.customer.choices.extend([(c.name, c.name) for c in customers])

    if reporfrm.validate_on_submit():
        from_date = datetime.strptime(reporfrm.date_from.data, '%d/%m/%Y')
        to_date = datetime.strptime(reporfrm.date_to.data, '%d/%m/%Y')

        data = []
        sum_data = 0
        report_type = reporfrm.report_type.data
        customer = reporfrm.customer.data

        if report_type == REPORT_TYPE_HOLIDAYS:
            p = Presta.query.join(Project) \
                .filter(Project.code == 'Off') \
                .filter(Presta.date >= from_date) \
                .filter(Presta.date <= (to_date + timedelta(days=1))) \
                .order_by(Presta.date).all()

            for i in p:
                presta = GenericObject()
                presta.date = i.date
                presta.description = i.description
                presta.hours = ("%.2f" % (i.duration / 3600.0))
                data.append(presta)
                sum_data += i.duration

            sum_data = (sum_data / 3600.0) / 8.0

        elif report_type == REPORT_TYPE_TRAVELS:
            p = Presta.query.join(Project) \
                .filter(Presta.travel_distance > 0) \
                .filter(Presta.date >= from_date) \
                .filter(Presta.date <= (to_date + timedelta(days=1))) \
                .order_by(Presta.date).all()

            for i in p:
                presta = GenericObject()
                presta.date = i.date
                presta.description = i.travel_comment
                presta.distance = i.travel_distance
                presta.project = i.project.code
                data.append(presta)
                sum_data += i.travel_distance

        elif report_type == REPORT_TYPE_PRESTAS:
                p = Presta.query.join(Project) \
                    .join(Customer) \
                    .filter(Project.code != 'Off') \
                    .filter(Customer.name.like(customer)) \
                    .filter(Presta.date >= from_date) \
                    .filter(Presta.date <= (to_date + timedelta(days=1))) \
                    .order_by(Customer.name) \
                    .order_by(Presta.date).all()

                for i in p:
                    presta = GenericObject()
                    presta.customer = i.project.customer.name
                    presta.project = i.project.code
                    presta.date = i.date
                    presta.description = i.description
                    presta.hours = ("%.2f" % (i.duration / 3600.0))
                    data.append(presta)
                    sum_data += i.duration

                sum_data = (sum_data / 3600.0) / 8.0

        return render_template('report.html', report=reporfrm, type=report_type, data=data, sum_data=sum_data)

    return render_template('report.html', report=reporfrm, type=None, data=None, sum_data=None)

@app.route('/admin/upload', methods = ['GET', 'POST'])
def upload_file():
    up = UploadForm()
    up.filetype.choices = [(f.identifier, f.description) for f in upload_file_types]
    up.customer.choices = [(c.name, c.name) for c in Customer.query.all()]

    if request.method == 'POST':
        # check if the post request has the file part
        if 'filename' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['filename']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        filename = secure_filename(file.filename)
        file.save(os.path.join('/tmp', filename))

        import_to_db(os.path.join('/tmp', filename), up.filetype.data)

        return redirect('/index')

    return render_template('upload.html', title="Upload File", up = up)
