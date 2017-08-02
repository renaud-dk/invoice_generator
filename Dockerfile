FROM ubuntu:16.04

RUN apt-get update

# Install python 3
RUN apt-get install -y build-essential python3 python3-dev python3-pip

# Weasy print dependnacies
RUN apt-get install -y python3-lxml python3-cffi libcairo2 libpango1.0-0 libgdk-pixbuf2.0-0 libffi-dev shared-mime-info

RUN python3 -m pip install wheel

COPY invoice_generator/ /invoice_generator
WORKDIR /invoice_generator

RUN pip3 install -r requirements.txt

# Start application
ENTRYPOINT ["python3"]
CMD ["run.py"]