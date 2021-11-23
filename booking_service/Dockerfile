FROM python:3.8-slim-buster

RUN mkdir booking_service
COPY . /booking_service/
WORKDIR /booking_service
RUN python -m pip install --upgrade pip
RUN python -m pip install -r requirements.txt

EXPOSE 8000
ENTRYPOINT [ "gunicorn", "--bind", "0.0.0.0:8000", "wsgi:app" ]