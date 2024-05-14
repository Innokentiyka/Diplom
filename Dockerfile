FROM python:3.11-alpine

ENV PYTHONDONTWRITEBYTECODE 1

ENV PYTHONBUFFERED 1

WORKDIR /http_service

COPY requirements.txt /http_service

RUN pip install -r requirements.txt

COPY . /http_service

EXPOSE 8000

CMD ["uvicorn","app:app","--host", "0.0.0.0", "--port", "8000", "--reload"]
