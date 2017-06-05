#-*- coding: utf-8 -*-
__author__ = 'rdk'

from flask import render_template, flash, request, redirect
from app import app, db
from app.models import Customer, Project
from app.forms import ProjectForm


@app.route('/project')
def project():
    projects = Project.query.join(Customer, Project.customer_id == Customer.id).order_by(Customer.name).all()
    return render_template('project.html', projects=projects)


@app.route('/new_project', methods=['GET', 'POST'])
def new_project():
    project = ProjectForm()
    project.customer.choices = [(c.id, c.name) for c in Customer.query.all()]
    if project.validate_on_submit():
        c = Customer.query.filter_by(id=project.customer.data).first()
        new_project = Project()

        new_project.code = project.code.data
        new_project.description = project.description.data


        c.projects.append(new_project)
        db.session.add(c)
        db.session.add(new_project)
        db.session.commit()

        flash('New project %s added for customer %s' % (project.code.data, c.name))

        return redirect('/index')
    return render_template('new_project.html', title="New project",
                           project=project)


@app.route('/project/edit/<pid>', methods = ['GET', 'POST'])
def edit_project(pid):
    pfrm = ProjectForm()
    pobj = Project.query.filter_by(id=pid).first()

    if request.method == 'GET':
        pfrm.customer.choices = [(c.id, c.name) for c in Customer.query.all()]
        pfrm.customer.data = pobj.customer_id

        pfrm.code.data = pobj.code
        pfrm.description.data = pobj.description

    else:
        # if pfrm.validate_on_submit():
        pobj.customer_id = pfrm.customer.data
        pobj.code = pfrm.code.data
        pobj.description = pfrm.description.data

        db.session.commit()

        flash('Project %s has been updated' % pobj.code)

        return redirect('/project')

    return render_template('new_project.html', title="Edit project",
                           project=pfrm)


@app.route('/project/delete/<pid>', methods = ['POST'])
def delete_project(pid):
    pobj = Project.query.filter_by(id=pid).first()

    db.session.delete(pobj)
    db.session.commit()

    flash('Project %s has been deleted' % pobj.code)

    return redirect('/project')