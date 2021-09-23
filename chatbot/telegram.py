import telebot, os, sys, re, json
sys.path.append(os.path.abspath("..")) # Agrega modulos N niveles abajo
from main import BOT_TELEGRAM_URI, N_TOPICOS_LIMITE
from comando import service

bot = telebot.TeleBot(BOT_TELEGRAM_URI)

ERROR_MSJ = '¡Lo siento! Hubo un error inesperado *~*'

def start():
	bot.polling()

def comm_info(args=None):
	comando = args[0] if args else None
	if comando=='lee':
		return "/lee" \
			   "\nArgumentos (obligatorios): url del sitio" \
			   "\nDescripción: lee, clasifica y guarda en tu biblioteca el artículo indicado" \
			   "\nUso: /lee {url}. Ejemplo: /lee https://towardsai.net/p/data-science/the-beginners-guide-to-elasticsearch"
	elif comando=='top':
		return "/top" \
			   "\nArgumentos (opcionales): número de topicos a listar (predeterminado 10 maximo 200)" \
			   "\nDescripción: obtiene una lista de los topicos y el número de artículos asociados. Ordenados de forma descendente" \
			   "\nUso: /top {numero}. Ejemplo: /top 15"
	elif comando=='topicos':
		return "/topicos" \
			   "\nDescripción: obtiene una lista de todos los topicos ordenados alfabéticamente" \
			   "\nUso: /topicos"
	else: return "/info" \
				 "\nArgumentos (opcionales): 'lee', 'top', 'topicos'"\
			   "\nDescripción: obtienes informacion cada comando para saber su forma de uso" \
			   "\nUso:/info {argumento}. Ejemplo: /info top"


@bot.message_handler(commands=['info','top','lee','topicos','trae'])
def command(message):
	d = separa_args(message.text)
	print('INPUT:',d)
	if d['comando']=='info':
		bot.reply_to(message, comm_info(d['args']))
	elif d['comando']=='lee':
		bot.reply_to(message, lee(d['args']))
	elif d['comando']=='top':
		bot.reply_to(message, top(d['args']))
	elif d['comando'] == 'topicos':
		bot.reply_to(message, topicos())
	elif d['comando'] == 'trae':
		bot.reply_to(message, trae(d['args']))
	else: bot.reply_to(message, comm_info())


def top(args=None):
	if not args:
		res = service.obtiene_top()
		print('obtiene_top',res)
		return '\n'.join(['{}: {}'.format(k, v) for k, v in res['data'].items()]) if res['ok'] else ERROR_MSJ
	else:
		parametro = service.try_generic(int,args[0])
		parametro = 10 if not parametro else parametro if parametro<N_TOPICOS_LIMITE else N_TOPICOS_LIMITE
		res = service.obtiene_top(lim_sup=parametro)
		print('obtiene_top',parametro,res)
		return '\n'.join(['{}: {}'.format(k,v) for k,v in res['data'].items()]) if res['ok'] else ERROR_MSJ

def lee(args):
	res = re.search('https?.+$', args[0]) if args else None
	if not res: return 'Lo siento no reconocí una URL válida, por favor intenta nuevamente.'
	url = res[0]
	# Verifica si no se ha guarado previamente esta url
	res = service.valida_url(url)
	print('valida_url',res)
	if not res['ok']: return ERROR_MSJ
	if res['data']: return 'Esta URL ya se ha procesado previamente.\nID: {}\nTítulo: {}\nModelo: {}'.format(
			res['data']['id'] if res['data'] else '',
			res['data']['titulo'] if res['data'] else '',
			res['data']['topic'] if res['data'] else '')
	else:
		res = service.procesa_url_nueva(url)
		print('procesa_url_nueva',res)
		if not res['ok']: return ERROR_MSJ
		else: return 'Al artículo "{}" se le asigna:\nID {}\nModelo: {}'.format(
				res['data']['titulo'] if res['data'] else '',
				res['data']['id'] if res['data'] else '',
				res['data']['topic'] if res['data'] else '')

def topicos():
	res = service.obtiene_topicos()
	print('obtiene_topicos', res)
	return str(res['data'].keys()).replace("'", "").replace(']', '').replace('[', '') if res['ok'] else ERROR_MSJ


def trae(args):
	if not args or (args and len(args)==0): return 'Se requiere al menos un topico, por favor intenta nuevamente.'
	res = service.valida_topicos(args)
	print('valida_topicos', res)
	if not res['ok']: return ERROR_MSJ
	if not res['data']: return '¡Lo siento! Alguno de los topicos dados no existe'
	res = service.comando_trae(args)
	print('comando_trae',res)
	if not res['ok']: return ERROR_MSJ
	return '\n'.join(res['data'])


def separa_args(texto):
	aux = texto.lower().strip().split(' ')
	return {'comando':aux[0].replace('/',''), 'args':[x for x in aux[1:] if len(x)>0] if len(aux)>1 else None}

