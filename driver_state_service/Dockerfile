FROM python:3.8-slim-buster

RUN mkdir driver_state_service
COPY . /driver_state_service/
WORKDIR /driver_state_service
RUN python -m pip install --upgrade pip
RUN python -m pip install -r requirements.txt

EXPOSE 8000
ENTRYPOINT [ "gunicorn", "-b", "0.0.0.0:8000", "--env", "DJANGO_SETTINGS_MODULE=driver_state_service.settings", "driver_state_service.wsgi" ]