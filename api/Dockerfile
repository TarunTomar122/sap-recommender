FROM python:3.10

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

ENTRYPOINT ["python"]

EXPOSE 8080

CMD ["app.py"]