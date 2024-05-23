FROM ubuntu:20.04

RUN apt update \
    && apt install -y python3 python3-pip \
    && cd /usr/bin \
    && ln -s python3 python

ADD ./b4cklog /mnt/b4cklog
ADD ./b4cklog_site /mnt/b4cklog_site
ADD ./media /mnt/media
ADD ./users /mnt/users
ADD ./manage.py /mnt/manage.py
ADD ./options.py /mnt/options
ADD ./requirements.txt /mnt/requirements.txt

EXPOSE 8000

CMD ["/bin/sh", "-c", "cd /mnt && python -m pip install -r requirements.txt && python manage.py makemigrations && python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
