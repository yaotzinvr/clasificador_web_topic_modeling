FROM python:3.6

RUN mkdir /app
WORKDIR /app

COPY /requirements.txt /app/
RUN pip install -r requirements.txt
COPY . /app

#CMD ["python", "./main.py"]

# docker build -t clasificador_web .
# docker run --rm -it --name clasificador clasificador_web