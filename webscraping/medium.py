from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import sys, os
sys.path.append(os.path.abspath(".."))
from main import SELENIUM_DRIVER_PATH

def nodo_articulo(artculo_url):
    try:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome(chrome_options=chrome_options) \
            if 'DEPLOY' in os.environ else \
            webdriver.Chrome(SELENIUM_DRIVER_PATH, chrome_options=chrome_options)
        driver.get(artculo_url)
        articulo = driver.find_element_by_tag_name('article')
    except Exception as e:
        raise Exception('(extraccion_contenido.nodo_articulo)'+str(e))
        # return {'ok': False, 'code': 500, 'msj': 'Error extraccion_contenido.nodo_articulo','error': str(e)}
    return {'ok': True,'data':articulo}

def extrae_contenido(artculo_url):
    try:
        article = nodo_articulo(artculo_url)['data']
        elementos_h1 = article.find_elements_by_tag_name('h1')
        titulo = ' '.join([x.text for x in elementos_h1]) if len(elementos_h1)>0 else ''
        elementos_h2 = article.find_elements_by_tag_name('h2')
        subtitulo = (
            ' '.join([elementos_h2[i].text for i in [0,1]]) if len(elementos_h2)>1 else elementos_h2[0].text
                    ) if len(elementos_h2)>0 else ''
        contenido = ' '.join([' '.join([x.text for x in article.find_elements_by_tag_name(x)]) for x in ['li','p']])
    except Exception as e:
        raise Exception('(extraccion_contenido.extrae_contenido)' + str(e))
        # return {'ok': False, 'code': 500, 'msj': 'ERROR (extraccion_contenido.extrae_contenido)','error': str(e)}
    return {'titulo':titulo,'subtitulo':subtitulo,'contenido':contenido}

if __name__ == '__main__':
    artculo_url = 'https://medium.com/towards-artificial-intelligence/topic-modeling-open-source-tool-fbdcc06f43f6'
    print(extrae_contenido(artculo_url))
