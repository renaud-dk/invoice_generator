#-*- coding: utf-8 -*-
__author__ = 'rdk'

import csv
from datetime import timedelta, datetime
from app import db, FILE_TYPE_PRJ, FILE_TYPE_PST
from app.models import Project, Customer, Presta


def import_to_db(filename, filetype):
    c = Customer.query.filter_by(name="Genitek Engineering").first()

    with open(filename, 'r') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',', quotechar='"')

        if filetype == FILE_TYPE_PRJ:
            for row in reader:
                new_project = Project()

                new_project.code = row['Code']
                new_project.description = row['Description']

                c.projects.append(new_project)
                db.session.add(c)
                db.session.add(new_project)
        elif filetype == FILE_TYPE_PST:
            for row in reader:
                project = Project.query.filter_by(code=row['Project']).first()

                if project is None:
                    print("Could not find project with code [" + row['Project'] + "]")
                else:
                    presta = Presta.query.join(Project) \
                        .filter(Project.code == row['Project']) \
                        .filter(Presta.date == datetime.strptime(row['Date'], '%d/%m/%Y %H:%M')).first()

                    if presta is not None:
                        print("Presta on date %s for project %s already exist" % (row['Date'], row['Project']))
                    else:
                        new_presta = Presta()
                        new_presta.project_id = project.id
                        new_presta.description = row['Description']

                        duration = datetime.strptime(row['Duration'], '%H:%M')
                        new_presta.duration = timedelta(hours=duration.hour, minutes=duration.minute).seconds

                        new_presta.date = datetime.strptime(row['Date'], '%d/%m/%Y %H:%M')

                        project.prestas.append(new_presta)
                        db.session.add(project)
                        db.session.add(new_presta)
        else:
            return

    db.session.commit()
