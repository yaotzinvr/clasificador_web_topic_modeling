FROM ursalab/amd64-ubuntu-18.04-conda-python-3.8
RUN apt update #&& apt-get install -y supervisor redis-server
RUN apt install -y chromium-browser

#RUN apt install -y python3.8
#RUN apt install -y python3-pip #python3-dev
#RUN apt remove python-pip
#RUN apt install -y python3-venv

RUN mkdir /app
WORKDIR /app

#RUN python3 -m venv /virtualenv
#RUN . /virtualenv/bin/activate

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt


COPY ./ /app
WORKDIR /app



#CMD ["python", "./database.py"]
#CMD ["python", "./chatbot.py"]


# docker build -t clasificador_web .
# docker run --rm -it --name clasificador clasificador_web