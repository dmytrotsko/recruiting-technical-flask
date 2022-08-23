FROM python:3.8-alpine
RUN apk add --no-cache mariadb-dev build-base libffi-dev gcc
COPY /api /app
COPY requirements.txt /app
WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["main.py"]
