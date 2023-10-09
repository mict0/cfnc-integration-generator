FROM --platform=linux/amd64 python:3.9-slim


ARG FOLDER=/dist

COPY .$FOLDER/deps/*.whl ./
RUN pip install *.whl && rm -rf *.whl

COPY .$FOLDER/*.whl ./
RUN pip install *.whl && rm -rf *.whl

