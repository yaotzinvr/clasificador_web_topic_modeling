import negocio
from config import N_TOPICOS_LIMITE

import webscraping
def servicio_add(url): return webscraping.extrae_contenido(url)

def servicio_add_(url):
    try:
        if len(list(negocio.get_categorias_all().keys())) > N_TOPICOS_LIMITE:
            return {'ok': True, 'msj': 'No se pueden agregar más artículos. Ya se ha superado el límite máximo de tópicos permitidos ({}).\nModifica la configuración o elimina artículos de tu bilblioteca'.format(N_TOPICOS_LIMITE)}
        articulos = negocio.get_articulo_by_url(url)
        if not articulos==None:
            return {'ok': True, 'msj': 'Esta URL ya se ha procesado previamente.\nID: {}\nTítulo: {}'.format(articulos['id'],articulos['titulo']) }
        res = negocio.procesa_url_nueva(url)
    except Exception as e:
        return {'ok': False, 'msj': 'ERROR (servicio_add)'+str(e)}
    return {'ok': True, 'msj':  'Guardado correctamente.\nID {}\nModelo: {}'.format(res['titulo'],res['id'],res['lda'])}


def servicio_rm(id_articulo):
    try:
        x = negocio.elimina_articulo(id_articulo)
        if x==0:
            return {'ok':True,'msj':'ID inválido'}
    except Exception as e:
        return {'ok': False, 'msj': 'ERROR (servicio_rm)'+str(e)}
    return {'ok': True, 'msj':  'Eliminado correctamente'}


def servicio_get(categorias):
    try:
        if len(categorias)==0:
            return {'ok': True, 'msj': 'Se requiere al menos una categoría'}
        valida_topicos = negocio.valida_topicos_no_existentes(categorias)
        if not len(valida_topicos)==0:
            return {'ok': True, 'msj': 'Estas categorías no con válidas: '+', '.join(valida_topicos)}
        urls_filtradas = negocio.get_urls_by_categorias(categorias)
    except Exception as e:
        return {'ok': False, 'msj': 'ERROR (servicio_get)'+str(e)}
    return {'ok': True, 'msj': '{} Resutado(s)\n - {}'.format(len(urls_filtradas),'\n - '.join(urls_filtradas))}

def servicio_top(N=None,top=True):
    try:
        categorias = negocio.get_categorias_all_sorted(N,top)
        res = '\n'.join(['({}) {}'.format(v,k) for k,v in categorias.items()])
    except Exception as e:
        return {'ok': False, 'msj': 'ERROR (servicio_top)'+str(e)}
    return {'ok': True, 'msj': res}


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
