import negocio
from config import LIMITE_MAX_ARTICULOS

def servicio_add(url):
    try:
        if not negocio.verifica_limite_articulos():
            return {'ok': True,
                    'msj': 'No se pueden agregar más artículos. Ya se ha llegado al límite máximo permitido ({}).\nModifica la configuración o elimina artículos de tu bilblioteca'.format(
                        LIMITE_MAX_ARTICULOS)}
        articulos = negocio.get_articulo_by_url(url)
        if not articulos==None:
            return {'ok': True, 'msj': 'Esta URL ya se ha procesado previamente.\nID: {}\nTítulo: {}'.format(articulos['id'],articulos['titulo']) }
        res = negocio.procesa_url_nueva(url)
    except Exception as e:
        return {'ok': False, 'msj': 'ERROR (servicio_add)'+str(e)}
    return {'ok': True, 'msj':  'Guardado correctamente.\nTítulo: {}\nID: {}\nCategorías: {}'.format(res['titulo'],res['id'],','.join(list(res['lda'].keys())))}


def servicio_rm(id_articulo):
    try:
        x = negocio.elimina_articulo(id_articulo)
        if x==0:
            return {'ok':True,'msj':'ID inválido'}
    except Exception as e:
        return {'ok': False, 'msj': 'ERROR (servicio_rm)'+str(e)}
    return {'ok': True, 'msj':  'Eliminado correctamente'}


def servicio_getc(categorias):
    try:
        if len(categorias)==0:
            return {'ok': True, 'msj': 'Se requiere al menos una categoría'}
        valida_topicos = negocio.valida_topicos_no_existentes(categorias)
        if not len(valida_topicos)==0:
            return {'ok': True, 'msj': 'Estas categorías no con válidas: '+', '.join(valida_topicos)}
        articulos = negocio.get_articulos_by_categorias(categorias)
        art = ['({})({}) {}'.format(str(x['_id']), x['titulo'], x['url']) for x in articulos]
    except Exception as e:
        return {'ok': False, 'msj': 'ERROR (servicio_get)'+str(e)}
    #return {'ok': True, 'msj': '{} Resutado(s)\n - {}'.format(len(urls_filtradas),'\n - '.join(['({}){}'.format(id,url) for id,url in urls_filtradas.items()]))}
    return {'ok': True, 'msj': '{} Resutado(s)\n - {}'.format(len(art), '\n - '.join(art))}

def servicio_get(texto):
    try:
        articulos = negocio.get_articulos_by_nombre(texto)
        art = ['({})({}) {}'.format(str(x['_id']), x['titulo'], x['url']) for x in articulos]
    except Exception as e:
        return {'ok': False, 'msj': 'ERROR (servicio_get)'+str(e)}
    return {'ok': True, 'msj': '{} Resutado(s)\n - {}'.format(len(art),'\n - '.join(art))}

def servicio_top(N=None,top=True):
    try:
        categorias = negocio.get_categorias_all_sorted(N,top)
        res = '\n'.join(['({}) {}'.format(v,k) for k,v in categorias.items()])
    except Exception as e:
        return {'ok': False, 'msj': 'ERROR (servicio_top)'+str(e)}
    return {'ok': True, 'msj': res}

def servicio_build():
    try:
        negocio.re_categotiza_todos_articulos()
    except Exception as e:
        return {'ok': False, 'msj': 'ERROR (servicio_build)'+str(e)}
    return {'ok': True, 'msj': 'Todos los artículos se han categorizado correctamente'}



# ********
# GENERICOS
# ********


def try_generic(f,arg):
    res = None
    try: res = f(arg)
    except Exception as e: print('try f: {}, agr: {}'.format(f,arg),e)
    return res


if __name__ == '__main__':
    artculo_url = 'https://medium.com/analytics-vidhya/supervised-ml-algorithm-support-vector-machines-svm-fb674430ab74'
    #print(servicio_add(artculo_url))
    print(servicio_top())
