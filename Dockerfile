FROM python:3.13-slim

# Install system dependencies required for building C-extensions (like tgcrypto)
RUN apt-get update -y && apt-get upgrade -y \
    && apt-get install -y --no-install-recommends gcc python3-dev build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app/
COPY . /app/

RUN pip3 install --no-cache-dir --upgrade pip
RUN pip3 install --no-cache-dir -U -r requirements.txt

CMD bash start
