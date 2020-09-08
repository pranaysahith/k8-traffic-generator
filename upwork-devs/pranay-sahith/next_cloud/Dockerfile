FROM python:3.7-stretch
WORKDIR /app

RUN apt update -y && apt install -y apt-transport-https
RUN curl -sSL https://dl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN echo "deb [arch=amd64] https://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list
RUN apt update -y && apt install -y google-chrome-stable
COPY ./requirements.txt /app/requirements.txt
RUN useradd -u 4999 -m test_runner
RUN chown test_runner: /app
USER test_runner
RUN pip install -r requirements.txt --user
COPY . /app
CMD [ "python", "main.py" ]
