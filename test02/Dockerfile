FROM python:3.8-slim
RUN pip install --upgrade pip
RUN apt install -y chromium-browser

RUN mkdir /app
WORKDIR /app

COPY /requirements.txt /app/
RUN pip install -r requirements.txt



COPY . /app



#CMD ["python", "./database.py"]
#CMD ["python", "./chatbot.py"]


# docker build -t clasificador_web .
# docker run --rm -it --name clasificador clasificador_web