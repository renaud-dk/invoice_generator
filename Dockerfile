FROM python:3.6-slim

RUN apt-get update && apt-get install -y libcairo2 libpango1.0-0 libgdk-pixbuf2.0-0 libffi-dev shared-mime-info sqlite3

WORKDIR /invoice_generator

#ADD ./config.py /invoice_generator
#ADD ./run.py /invoice_generator
ADD ./requirements.txt /invoice_generator
#ADD ./app /invoice_generator/app
#ADD ./database/app.db /invoice_generator/database/app.db

RUN pip install --trusted-host pypi.python.org -r requirements.txt
EXPOSE 8080

# Start application
CMD ["python", "run.py"]
