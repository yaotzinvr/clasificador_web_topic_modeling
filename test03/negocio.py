import database
import model
import webscraping
import functools
from config import LIMITE_MAX_ARTICULOS

def get_articulo_by_url(url):
    try:
        res = database.get({'url':url},atributos=['_id','url','titulo','lda'])
        articulos = res[0] if len(res) > 0 else None
        if articulos: articulos['id'] = articulos.pop('_id')
    except Exception as e:
        raise Exception('(get_articulo_by_url)' + str(e))
    return articulos

def verifica_limite_articulos():
    try:
        articulos = database.get(None, atributos=['_id'])
        n_arts = len(list(articulos))
        print(LIMITE_MAX_ARTICULOS,n_arts)
    except Exception as e:
        raise Exception('(verifica_limite_articulos)' + str(e))
    return LIMITE_MAX_ARTICULOS > n_arts

def procesa_url_nueva(url):
    try:
        print('Comienza extraccion a ', url)
        contenido_web = webscraping.extrae_contenido(url)
        texto_completo = ' '.join(contenido_web.values())
        print('Obtiene modelo LDA')
        model_lda = model.get_model(texto_completo)
        print('Guarda en BD')
        id = database.save(
            {'titulo': contenido_web['titulo'],
             'subtitulo': contenido_web['subtitulo'],
             'lda': model_lda,
             'url': url,
             'contenido': contenido_web['contenido']}
        )
    except Exception as e:
        raise Exception('(procesa_url_nueva)' + str(e))
    return {'id': id, 'titulo': contenido_web['titulo'], 'lda': model_lda}

def elimina_articulo(id_articulo):
    try:
        x = database.delete(id_articulo)
        print(x)
    except Exception as e:
        raise Exception('(elimina_articulo)' + str(e))
    return x


# Indica si los topicos se encuentran realmente en la coleccion
def valida_topicos_no_existentes(topicos_usuario):
    try:
        topicos = [k for k in get_categorias_all().keys()]
        # Determino si todos los topicos_usuario estan dentro de los topicos de la coleccion
        no_existen = [t in topicos for t in topicos_usuario]
    except Exception as e:
        raise Exception('(valida_topicos_no_existentes)' + str(e))
    return [topicos_usuario[i] for i,x in enumerate(no_existen) if not x]

def get_articulos_by_categorias(categorias):
    try:
        # Hago un diccionario de urls con sus topicos
        articulos = database.get(None, atributos=['_id', 'titulo' ,'url', 'lda'])
        urls_topicos = {}
        for x in articulos:
            urls_topicos[x['url']] = [t for t,v in x['lda'].items()]
        # Detecto y guardo unicamente las URLs con los topicos especificados
        urls_filtradas = []
        for url, topics in urls_topicos.items():
            if functools.reduce(lambda A, B: A and B, [c in topics for c in categorias]):
                urls_filtradas.append(url)
        arts=[]
        for x in articulos:
            if x['url'] in urls_filtradas: arts.append(x)
    except Exception as e:
        raise Exception('(get_articulos_by_categorias)' + str(e))
    return arts

def get_articulos_by_nombre(texto):
    try:
        articulos = database.get({"titulo": {"$regex": texto, "$options": 'i'}}, atributos=['_id', 'titulo', 'url','lda'])
    except Exception as e:
        raise Exception('(get_articulos_by_nombre)' + str(e))
    return list(articulos)


# Obtiene topicos ordenados
def get_categorias_all_sorted(N=None,top=True):
    try:
        d = get_categorias_all()
        ordenados = {k: v for k, v in
            {k: v for k, v in sorted(d.items(), key=lambda item: item[1], reverse=top)}
                .items()}
        N = N if N else len(ordenados)
        ordenados_filtrados = {k:v for i,(k,v) in enumerate(ordenados.items()) if i<N}
    except Exception as e: raise Exception('(get_categorias_all_sorted)' + str(e))
    return ordenados_filtrados

# Obtiene todos los topicos, en desorden
def get_categorias_all():
    try:
        articulos = database.get(None, atributos=['_id', 'titulo', 'lda'])
        d = {}
        for x in articulos:
            for topico, valor in x['lda'].items(): d[topico] = d[topico] + 1 if topico in d else 1
    except Exception as e: raise Exception('(get_categorias_all)' + str(e))
    return d

def re_categotiza_todos_articulos():
    try:
        articulos = database.get(None, atributos=['_id', 'titulo', 'subtitulo', 'contenido'])
        for x in articulos:
            model_lda = model.get_model('{} {} {}'.format(x['titulo'],x['titulo'],x['contenido']))
            database.update_by_id(x['_id'],{'lda': model_lda})
    except Exception as e: raise Exception('(re_categotiza_todos_articulos)' + str(e))


if __name__ == '__main__2':
    url = 'https://medium.com/@TCWstrategies/machine-learning-and-progressive-organizing-now-is-the-time-e9ce2a429b1a'
    contenido_web = webscraping.extrae_contenido(url)
    print(contenido_web['titulo'])
    texto_completo = ' '.join(contenido_web.values())
    model_lda = model.get_model(texto_completo)
    print(', '.join(list(model_lda.keys())))
    #print(get_categorias_all_sorted(5))

if __name__ == '__main__':
    #print(get_urls_by_categorias(['data']))
    #print(procesa_url_nueva('https://medium.com/@arpit2412/cross-entropy-but-not-without-entropy-and-kl-divergence-a8782b41eebe'))
    print(verifica_limite_articulos())