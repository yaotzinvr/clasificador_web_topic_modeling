# base image
FROM python:3.6
#Permisos
#USER root
# set working directory
RUN mkdir /app
WORKDIR /app
# install dependencies
COPY /requirements.txt /app/
RUN pip install -r requirements.txt
#Copiamos archivos
COPY . /app
RUN python /app/download_stopwords.py
# start app
#CMD ["python", "start.py"]