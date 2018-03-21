FROM python:latest

RUN pip install numpy && \
    pip install PyMongo && \
    pip install Flask && \
    pip install Flask_restful && \
    pip install docker && \
    pip install recastai


RUN curl -L https://github.com/docker/compose/releases/download/1.19.0/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose
RUN chmod +x /usr/local/bin/docker-compose

CMD ["python", "src/main.py"]
