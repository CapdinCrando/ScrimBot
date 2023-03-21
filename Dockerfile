FROM python:3.10-slim

WORKDIR /scrimbot

ADD cogs .
ADD games .
ADD bot_config.py .
ADD scrim_bot.py . 
ADD requirements.txt .

RUN apt-get -y update
RUN apt-get install -y ffmpeg
RUN pip install -r requirements.txt

CMD ["python", "./scrim_bot.py"]