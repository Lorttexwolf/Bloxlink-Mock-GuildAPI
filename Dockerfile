FROM python:3.10.9

ADD . .
RUN pip install sanic requests python-dotenv

EXPOSE 8001:8001

ENTRYPOINT ["python", "./src/main.py"]