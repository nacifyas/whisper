FROM python:3.11-slim

RUN export DEBIAN_FRONTEND=noninteractive \
    && apt update \
    && apt install --no-install-recommends ffmpeg -y \
    && rm -rf /var/lib/apt/lists/*

ARG TZ
RUN echo ${TZ} > /etc/timezone

WORKDIR /whisper

COPY . /whisper

RUN pip install --no-cache-dir --upgrade /whisper/.

EXPOSE 8000

CMD [ "python3", "/whisper/app/main.py" ]
