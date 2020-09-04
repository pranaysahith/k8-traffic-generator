FROM alpine:3.12 AS permissions-giver
# Make sure docker-entrypoint.sh is executable, regardless of the build host.
WORKDIR /out
COPY docker-entrypoint.sh .
RUN chmod +x docker-entrypoint.sh

FROM alpine:3.12 AS organizer
WORKDIR /out/usr/local/bin
COPY --from=permissions-giver /out/docker-entrypoint.sh .
WORKDIR /out/usr/src/app
COPY . .

FROM python:3.6 AS dependency-installer
WORKDIR /usr/src/app
COPY requirements.txt .
RUN pip install -r requirements.txt &&\
    python -c "from pyppeteer.chromium_downloader import download_chromium; download_chromium()" &&\
    apt-get update && \
    apt-get install -y \
    ca-certificates \
    fonts-liberation \
    libappindicator3-1 \
    libasound2 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libc6 \
    libcairo2 \
    libcups2 \
    libdbus-1-3 \
    libexpat1 \
    libfontconfig1 \
    libgbm1 \
    libgcc1 \
    libglib2.0-0 \
    libgtk-3-0 \
    libnspr4 \
    libnss3 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libstdc++6 \
    libx11-6 \
    libx11-xcb1 \
    libxcb1 \
    libxcomposite1 \
    libxcursor1 \
    libxdamage1 \
    libxext6 \
    libxfixes3 \
    libxi6 \
    libxrandr2 \
    libxrender1 \
    libxss1 \
    libxtst6 \
    lsb-release \
    wget \
    xdg-utils

FROM dependency-installer AS runner
COPY --from=organizer /out /
ENV MODE=traffic \
    URL=https://glasswallsolutions.com/
ENTRYPOINT [ "docker-entrypoint.sh" ]