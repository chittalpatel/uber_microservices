FROM python:3.8-slim-buster

RUN mkdir driver_state_service
COPY . /driver_state_service/
WORKDIR /driver_state_service
RUN python -m pip install --upgrade pip
RUN python -m pip install -r requirements.txt

EXPOSE 8000
ENTRYPOINT [ "python", "-u", "manage.py", "runserver" ]