
# GENERALES
# N_TOPICOS_LIMITE: indica la cantidad máxima de tópicos que puedes tener en tu biblioteca. También topa la cantidad de artículos que puedes tener
LIMITE_MAX_ARTICULOS = 8
# CATEGORIAS_EXCLUIR: indica las categorías que NO se tomarpan en cuenta al generar el modelo LDA
CATEGORIAS_EXCLUIR = ['entropy','true','cross']

# CHATBOT
# BOT_TELEGRAM_URI: token de conexión con el chatbot de telegram
BOT_TELEGRAM_URI = '5003545517:AAFP-BnWwR2TngHRLPoAJD5IcPEwT9pLBKY'

# BASE DE DATOS
BD = 'topic_modeling'
COLLECTION = 'articulos'
# MONGO_URI: cadena de conexión a la base de datos de MongoDB
MONGO_URI='mongodb://usuario:pass@127.0.0.1:27017/{}'.format(BD)
