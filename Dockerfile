FROM --platform=$BUILDPLATFORM python:3.11-slim

RUN export DEBIAN_FRONTEND=noninteractive \
    && app -qq update \
    && apt -qq install --no-install-recommends ffmpeg \
    && rm -rf /var/lib/lists/*

WORKDIR /whisper

COPY . /whisper

RUN pip install --no-cache-dir --upgrade /whisper/.

ENTRYPOINT [ "python3", "-m", "/whisper/app/main.py" ]
