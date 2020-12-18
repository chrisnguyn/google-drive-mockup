FROM python:latest

WORKDIR /usr/src/app

COPY . .

RUN pip3 install setuptools==45
RUN pip3 install --no-cache-dir -r requirements.txt

CMD python3 src/main.py
