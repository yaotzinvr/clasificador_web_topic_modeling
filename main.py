from . import envs

BOT_TELEGRAM_URI = envs.BOT_TELEGRAM_URI
MONGO_URI = envs.MONGO_URI
MODEL_ML_URI = 'http://0.0.0.0:55555'
SELENIUM_DRIVER_PATH = envs.SELENIUM_DRIVER_PATH

N_TOPICOS_LIMITE = 200

from chatbot import telegram

if __name__ == '__main__':
    telegram.start()