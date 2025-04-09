FROM python:3.10-slim

WORKDIR /app

ADD . .

RUN apt-get -y update
RUN apt-get install -y ffmpeg
RUN pip install -r requirements.txt

CMD ["python", "./bot.py"]
