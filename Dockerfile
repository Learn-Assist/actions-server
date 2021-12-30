FROM python:3.8.0-buster

WORKDIR /app/actions

COPY . .

USER root

RUN pip install rasa_sdk

RUN pip install sanic==21.9.3 requests

USER 1001

EXPOSE 5055

CMD ["python", "-m", "rasa_sdk", "--actions", "actions"]