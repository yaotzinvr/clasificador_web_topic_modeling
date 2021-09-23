import requests, json
from webscraping import medium
import sys, os
sys.path.append(os.path.abspath(".."))
from comando.db import get, save, update_many
from main import MODEL_ML_URI


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


# Valida si la URL dada ya se ha procesado anteriormente
def valida_url(url):
    try:
        res = get({'url':url},lista_variables=['_id','url','titulo','topic'])
        articulos = res[0] if len(res) > 0 else None
        articulos['id'] = articulos['_id']
    except Exception as e:
        return {'ok': False, 'code': 500, 'msj': 'ERROR (service.valida_url)', 'error': str(e)}
    return {'ok': True, 'data': articulos }

def reprocesa_articulo(articulo):
    print('Reconstruye modelo LDA para ',articulo['_id'])
    model_lda = __get_model(articulo['titulo']+' '+articulo['subtitulo']+' '+articulo['contenido'])
    articulo['topic'] = model_lda


def reorganiza_articulos():
    articulos = get(None)
    [reprocesa_articulo(x) for x in articulos]
    print('Guarda en BD')
    update_many(articulos)


# Procesa una URL por primera vez
def procesa_url_nueva(url):
    try:
        print('Comienza extraccion a ', url)
        contenido_web = medium.extrae_contenido(url)
        texto_completo = ' '.join(contenido_web.values())
        print('Obtiene modelo LDA')
        model_lda = __get_model(texto_completo)
        print('Guarda en BD')
        id = save(
            {'titulo': contenido_web['titulo'],
             'subtitulo': contenido_web['subtitulo'],
             'topic': model_lda,
             'url': url,
             'contenido': contenido_web['contenido']}
        )
    except Exception as e:
        return {'ok': False, 'code': 500, 'msj': 'ERROR (service.procesa_url)', 'error': str(e)}
    return {'ok': True, 'data': {'id':id, 'titulo':contenido_web['titulo'], 'topic':model_lda } }

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
        articulos = get(None, lista_variables=['_id', 'url', 'topic'])
        urls_topicos = {}
        for x in articulos:
            urls_topicos[x['url']] = [t for t,v in x['topic'].items()]
        # Detecto y guardo unicame las URLs con los topicos especificados
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
        articulos = get(None, lista_variables=['_id', 'titulo', 'topic'])
        d = {}
        for x in articulos:
            for topico, valor in x['topic'].items(): d[topico] = d[topico] + 1 if topico in d else 1
    except Exception as e: raise Exception('(service._obtiene_topicos)' + str(e))
    return d

def __get_model(texto_completo):
    try:
        res = requests.post(MODEL_ML_URI + '/topic-modeling/get',
                            json={'texto_completo': texto_completo},
                            headers={'Content-Type': 'application/json'},
                            verify=False)
        if res.status_code < 200 or res.status_code > 299:
            raise Exception('(service.__get_model)' + str(res))
        else:
            model_lda = json.loads(res.text)['topic']
    except requests.exceptions.ConnectionError as e:
        raise Exception('(service.__get_model)' + str(e))
    return dict(zip([x.split('*')[1] for x in model_lda.split(' + ')],[float(x.split('*')[0]) for x in model_lda.split(' + ')]))





if __name__ == '__main__':
    artculo_url = 'https://medium.com/towards-artificial-intelligence/topic-modeling-open-source-tool-fbdcc06f43f6'
    print(procesa_url_nueva(artculo_url))