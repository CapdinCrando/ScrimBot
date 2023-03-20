FROM python:3.10

RUN apk add --no-cache ffmpeg
RUN pip install -r requirements.txt

CMD ["python", "./scrim_bot.py"]