from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException

def extrae_contenido(artculo_url):
    try:
        #Genera nueva sesion
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        # Extrae contenido
        driver.get(artculo_url)
        article = driver.find_element(by=By.TAG_NAME,value='article')
        elementos_h1 = article.find_elements(by=By.TAG_NAME,value='h1')
        titulo = ' '.join([x.text for x in [e for i,e in enumerate(elementos_h1) if i<3] ]) if len(elementos_h1) > 0 else ''
        elementos_h2 = article.find_elements(by=By.TAG_NAME,value='h2')
        subtitulo = (
            ' '.join([elementos_h2[i].text for i in [0, 1]]) if len(elementos_h2) > 1 else elementos_h2[0].text
        ) if len(elementos_h2) > 0 else ''
        contenido = ' '.join([' '.join([x.text for x in article.find_elements(by=By.TAG_NAME,value=x)]) for x in ['li', 'p']])
        # Cierra sesion
        driver.quit()
    except NoSuchElementException as e:
        raise Exception('URL INVALIDA')
    except Exception as e:
        raise Exception('(extrae_contenido)'+str(e))
        # return {'ok': False, 'code': 500, 'msj': 'Error extraccion_contenido.nodo_articulo','error': str(e)}
    return {'titulo':titulo,'subtitulo':subtitulo,'contenido':contenido}


if __name__ == '__main__':
    artculo_url = 'https://medium.com/towards-artificial-intelligence/topic-modeling-open-source-tool-fbdcc06f43f6'
    print(extrae_contenido(artculo_url))
