FROM python:3.10.4


WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
COPY . .
#ADD cert.pem ./cert.pem
#ADD key.pem ./key.pem

RUN pip install django-recaptcha
RUN pip install django-otp captcha qrcode
RUN pip install pyOpenSSL
RUN pip install django
RUN pip install django_otp
RUN pip install django-extensions
RUN pip install Werkzeug

EXPOSE 443

#CMD [ "0.0.0.0:443","--cert-file ./cert.pem", "--key-file ./key.pem"]
#ENTRYPOINT [ "python", "./manage.py", "runserver_plus"]

#RUN python manage.py runserver_plus --cert-file cert.pem --key-file key.pem
CMD [ "python", "./manage.py", "runserver_plus", "0.0.0.0:443"]
