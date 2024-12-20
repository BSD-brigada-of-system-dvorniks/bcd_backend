FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    EDITOR=micro \
    DJANGO_SECRET=${DJANGO_SECRET} \
    DJANGO_DEBUG=${DJANGO_DEBUG} \
    DJANGO_DOMAIN=${DJANGO_DOMAIN} \
    MONGO_NAME=${MONGO_NAME} \
    MONGO_USER=${MONGO_USER} \
    MONGO_PASSWORD=${MONGO_PASSWORD} \
    MONGO_HOST=${MONGO_HOST} \
    MONGO_PORT=${MONGO_PORT}

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc micro && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip
COPY ./requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

EXPOSE 80

CMD ["/bin/sh", "-c", "\
    python manage.py collectstatic --noinput && \
    printenv | grep -v 'no_proxy' >> /etc/environment && \
    python manage.py runserver 0.0.0.0:80"]
