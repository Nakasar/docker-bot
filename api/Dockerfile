FROM python:latest

RUN pip install numpy && \
    pip install PyMongo && \
    pip install Flask && \
    pip install Flask_restful

ADD main.py /

CMD ["python", "main.py"]
