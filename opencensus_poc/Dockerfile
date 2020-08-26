FROM python:3.7-stretch
WORKDIR /app

COPY ./requirements.txt /app/requirements.txt
RUN useradd -u 4999 -m test_runner
USER test_runner
RUN pip install -r requirements.txt --user
COPY . /app
CMD [ "python", "main.py" ]
