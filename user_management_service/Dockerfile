FROM python:3.8-slim-buster

RUN mkdir user_service
COPY . /user_service/
WORKDIR /user_service
RUN python -m pip install --upgrade pip
RUN python -m pip install -r requirements.txt

EXPOSE 8000
ENTRYPOINT [ "python", "-u", "main.py" ]