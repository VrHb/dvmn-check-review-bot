FROM python:3.10

WORKDIR /code

COPY requirements.txt ./
COPY .env ./

RUN pip install -r requirements.txt

COPY *.py ./

ENTRYPOINT ["python", "main.py"]
