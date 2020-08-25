FROM python:3.6

RUN mkdir /app
WORKDIR /app
ADD . /app/
RUN pip install -r requirements.txt

CMD ["python", "/app/main.py", "-u", "https://glasswallsolutions.com/", "-a", "open"]
