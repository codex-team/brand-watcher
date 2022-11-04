FROM python:3.9-slim-buster

WORKDIR /home/app

RUN pip install --upgrade pip
COPY . .
RUN pip install -r requirements.txt
CMD ["python", "main.py"]
