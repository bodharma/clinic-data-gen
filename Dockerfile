FROM python:3.9
COPY . /
RUN pip3 install -r /requirements.txt
ENTRYPOINT uvicorn app:app --port 80 --host 0.0.0.0
