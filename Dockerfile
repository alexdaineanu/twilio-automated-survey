FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /survey
WORKDIR /survey
COPY requirements.txt /survey
RUN pip install -r requirements.txt
EXPOSE 80 8000
