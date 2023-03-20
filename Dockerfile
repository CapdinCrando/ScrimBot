FROM python:3.10

RUN apt-get install ffmpeg
RUN pip install -r requirements.txt

CMD ["python", "./scrim_bot.py"]