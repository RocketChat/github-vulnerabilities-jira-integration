FROM python:3.9

WORKDIR /app

COPY src .

RUN pip install --no-cache-dir -r src/requirements.txt

CMD [ "python", "main.py"]