FROM python:3.6 AS dependency-installer
WORKDIR /usr/src/app
COPY requirements.txt .
RUN pip install -r requirements.txt &&\
    python -c "from pyppeteer.chromium_downloader import download_chromium; download_chromium()"

FROM dependency-installer AS runner
COPY . .
CMD ["python", "main.py", "-u", "https://glasswallsolutions.com/", "-a", "open"]