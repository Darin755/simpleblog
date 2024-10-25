FROM python:3.9-slim

WORKDIR /usr/app

COPY requirements.txt requirements.txt

RUN pip install --upgrade pip

RUN pip3 install --no-cache-dir -r requirements.txt

COPY src .

EXPOSE 5000



CMD ["gunicorn", "app:app", "-b", "0.0.0.0:5000", "-w", "5"]
