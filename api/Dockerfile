FROM python:3.10-bullseye
WORKDIR /app
COPY . /app

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6 -y 

RUN pip install -r requirements.txt
EXPOSE 5000
CMD ["flask", "run", "--host", "0.0.0.0"]