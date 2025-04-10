FROM python:3.10-slim

WORKDIR /app

ADD . .

RUN apt-get -y update
RUN apt-get install -y ffmpeg

RUN python -m venv /app/env
RUN /app/env/bin/pip install -r requirements.txt

CMD ["/app/env/bin/python", "./bot.py"]
