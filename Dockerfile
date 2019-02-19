FROM python:3.6

RUN mkdir -p /opt/services/appcheck/src
WORKDIR /opt/services/appcheck/src


COPY . /opt/services/appcheck/src

ENV PATH "$PATH:.:.."
  
RUN pip3 install -r requirements.txt
RUN cd appcheck && python3 manage.py collectstatic --no-input 
