#-*- coding: utf-8 -*-
__author__ = 'rdk'


from flask import render_template, flash, request, redirect
from app import app, db
from app.models import Customer
from app.forms import CustomerForm


@app.route('/customer')
def customer():
    customers = Customer.query.all()
    return render_template('customer.html', customers=customers)


@app.route('/new_customer', methods=['GET', 'POST'])
def new_customer():
    customer = CustomerForm()
    if customer.validate_on_submit():
        flash('New customer %s added' % customer.name.data)
        new_customer = Customer()

        new_customer.name = customer.name.data
        new_customer.address = customer.address.data
        new_customer.city = customer.city.data
        new_customer.zip_code = customer.zip_code.data
        new_customer.country = customer.country.data
        new_customer.vat = customer.vat.data

        db.session.add(new_customer)
        db.session.commit()

        return redirect('/index')
    return render_template('new_customer.html', title="New customer",
                           customer=customer)


@app.route('/customer/edit/<cid>', methods = ['GET', 'POST'])
def edit_customer(cid):
    cfrm = CustomerForm()
    cobj = Customer.query.filter_by(id=cid).first()

    if request.method == 'GET':
        cfrm.name.data = cobj.name
        cfrm.address.data = cobj.address
        cfrm.city.data = cobj.city
        cfrm.zip_code.data = cobj.zip_code
        cfrm.country.data = cobj.country
        cfrm.vat.data = cobj.vat
    else:
        cobj.name = cfrm.name.data
        cobj.address = cfrm.address.data
        cobj.city = cfrm.city.data
        cobj.zip_code = cfrm.zip_code.data
        cobj.country = cfrm.country.data
        cobj.vat = cfrm.vat.data

        db.session.commit()

        flash('Customer %s has been updated' % cobj.name)

        return redirect('/customer')

    return render_template('new_customer.html', title="Edit customer",
                           customer=cfrm)


@app.route('/customer/delete/<pid>', methods = ['POST'])
def delete_customer(pid):
    cobj = Customer.query.filter_by(id=pid).first()

    db.session.delete(cobj)
    db.session.commit()

    flash('Customer %s has been deleted' % cobj.name)

    return redirect('/customer')