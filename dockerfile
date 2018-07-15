FROM python:3
RUN apt-get update \
  && apt-get install -y curl python3 python3-pip
COPY . /usr/local/bin/homeapi/
WORKDIR /usr/local/bin/homeapi
RUN pip3 --no-cache-dir install -r requirements.txt
EXPOSE 8000
ENTRYPOINT ["/usr/local/bin/gunicorn", "-b", ":8000", "wsgi"]
