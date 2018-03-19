FROM python:latest

RUN pip install numpy
RUN pip install PyMongo
RUN pip install Flask
RUN pip install Flask_restful

ADD main.py /

CMD ["python", "main.py"]
