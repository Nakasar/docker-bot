FROM python:latest

RUN pip install numpy && \
    pip install PyMongo && \
    pip install Flask && \
    pip install Flask_restful

RUN apt-get install \
     apt-transport-https \
     ca-certificates \
     curl \
     gnupg2 \
     software-properties-common

RUN curl -fsSL https://download.docker.com/linux/debian/gpg | sudo apt-key add -
RUN add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/debian \
   $(lsb_release -cs) \
   stable"

RUN deb-src [arch=amd64] https://download.docker.com/linux/debian wheezy stable

RUN apt-get update && \
  apt-get install docker-ce docker-compose

#ADD src/main.py /src/

CMD ["python", "src/main.py"]
