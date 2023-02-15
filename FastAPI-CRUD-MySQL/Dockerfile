FROM ubuntu:20.04

RUN apt-get update -qq \
    && apt-get install -y software-properties-common vim \
    && apt-get install -y --no-install-recommends build-essential \
    && apt-get install -y python3-pip libpq-dev python3-dev \
    && apt-get install -y default-libmysqlclient-dev \
    && cd /usr/local/bin \
    && pip3 install --upgrade pip \
    && apt-get clean

# Upgrading packages to install latest OS fixes
RUN apt-get upgrade -y
WORKDIR /app
COPY . .
RUN pip3 install -r requirements.txt 
RUN ["chmod","+x","/app/src/main.py"]
EXPOSE 8200
CMD ["python3", "src/main.py"]