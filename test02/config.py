
# GENERALES
# N_TOPICOS_LIMITE: indica la cantidad máxima de tópicos que puedes tener en tu biblioteca. También topa la cantidad de artículos que puedes tener
N_TOPICOS_LIMITE = 200

# CHATBOT
# BOT_TELEGRAM_URI: token de conexión con el chatbot de telegram
BOT_TELEGRAM_URI = '5003545517:AAFP-BnWwR2TngHRLPoAJD5IcPEwT9pLBKY'

# BASE DE DATOS
BD = 'topic_modeling'
COLLECTION = 'articulos'
# MONGO_URI: cadena de conexión a la base de datos de MongoDB
MONGO_URI='mongodb://usuario:pass@127.0.0.1:27017/{}'.format(BD)
