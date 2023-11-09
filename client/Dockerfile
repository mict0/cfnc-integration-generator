FROM --platform=linux/amd64 python:3.9-slim

RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

ARG FOLDER=/dist

COPY .$FOLDER/deps/*.whl ./
RUN pip install *.whl && rm -rf *.whl

COPY .$FOLDER/*.whl ./
RUN pip install *.whl && rm -rf *.whl

