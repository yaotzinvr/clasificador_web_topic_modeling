import requests
import webscraping
from database import get, save, update_many, update_one
import model

# Ordena los topicos de manera alfabetica
def obtiene_topicos():
    try:
        d = __obtiene_topicos()
    except Exception as e:
        return {'ok': False, 'code': 500, 'msj': 'ERROR (service.obtiene_topicos)', 'error': str(e)}
    return {'ok': True, 'data': {k: v for k, v in sorted(d.items(), key=lambda item: item[0])}}

# Obtiene los primeros N topicos de acuerdo a su popularidad
def obtiene_top(lim_inf=0,lim_sup=10):
    try:
        d = __obtiene_top_all()
    except Exception as e: return {'ok': False, 'code': 500, 'msj': 'ERROR (service.obtiene_top)', 'error': str(e)}
    return {'ok': True, 'data': {k: v for k, v in list(d.items())[lim_inf:lim_sup] }}

# Obtiene el valor de N_TOPICOS_LIMITE
def verifica_N_TOPICOS_LIMITE():
    try:
        x=50
    except Exception as e:
        return {'ok': False, 'code': 500, 'msj': 'ERROR (service.verifica_N_TOPICOS_LIMITE)', 'error': str(e)}
    return {'ok': True, 'data': x }







def reorganiza_articulos():
    articulos = get(None)
    [reprocesa_articulo(x) for x in articulos]
    print('Guarda en BD')
    update_many(articulos)



# Indica si los topicos se encuentran realmente en la coleccion
import functools as f
def valida_topicos(topicos_usuario):
    try:
        topicos = [k for k in __obtiene_topicos().keys()]
        # Determino si todos los topicos_usuario estan dentro de los topicos de la coleccion
        existen_todos = True
        for t in topicos_usuario:
            existen_todos = t in topicos
            if not existen_todos: break
    except Exception as e:
        return {'ok': False, 'code': 500, 'msj': 'ERROR (service.valida_topicos)', 'error': str(e)}
    return {'ok': True, 'data': existen_todos }

# Trae las URL que coincidan con los parametros dados
def comando_trae(topicos_usuario):
    try:
        # Hago un diccionario de urls con sus topicos
        articulos = get(None, lista_variables=['_id', 'url', 'lda'])
        urls_topicos = {}
        for x in articulos:
            urls_topicos[x['url']] = [t for t,v in x['lda'].items()]
        # Detecto y guardo unicamente las URLs con los topicos especificados
        urls_filtradas = []
        for url, topics in urls_topicos.items():
            if f.reduce(lambda A, B: A and B in topics, topicos_usuario):
                urls_filtradas.append(url)
    except Exception as e:
        return {'ok': False, 'code': 500, 'msj': 'ERROR (service.comando_trae)', 'error': str(e)}
    return {'ok': True, 'data': urls_filtradas }



def try_generic(f,arg):
    res = None
    try: res = f(arg)
    except Exception as e: print('try f: {}, agr: {}'.format(f,arg),e)
    return res


# ********
# PRIVADOS
# ********

# Obtiene todos los topicos de acuerdo a su popularidad
def __obtiene_top_all():
    try:
        d = __obtiene_topicos()
    except Exception as e: raise Exception('(service.__obtiene_top_all)' + str(e))
    return {k: v for k, v in
            {k: v for k, v in sorted(d.items(), key=lambda item: item[1], reverse=True)}
                .items()}

# Obtiene todos los topicos, en desorden
def __obtiene_topicos():
    try:
        articulos = get(None, lista_variables=['_id', 'titulo', 'lda'])
        d = {}
        for x in articulos:
            for topico, valor in x['lda'].items(): d[topico] = d[topico] + 1 if topico in d else 1
    except Exception as e: raise Exception('(service._obtiene_topicos)' + str(e))
    return d







if __name__ == '__main__':
    artculo_url = 'https://medium.com/analytics-vidhya/supervised-ml-algorithm-support-vector-machines-svm-fb674430ab74'
    #artculo_url = 'https://medium.com/towards-artificial-intelligence/topic-modeling-open-source-tool-fbdcc06f43f6'
    print(get_articulo_by_url(artculo_url))
    #print(procesa_url_nueva()

    #print(comando_trae(['data','python']))