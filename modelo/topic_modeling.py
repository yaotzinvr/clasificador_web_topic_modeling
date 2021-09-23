import re
import gensim
from gensim.utils import simple_preprocess
import gensim.corpora as corpora
# import nltk
# Solo se descarga la primera vez
# nltk.download('stopwords')
from nltk.corpus import stopwords
stop_words = stopwords.words('english')

stop_words.extend(['lack', 'make', 'want', 'seem', 'run', 'need', 'even', 'right',
'use', 'not', 'would', 'say', 'could', '_', 'be', 'know', 'good', 'go', 'get', 'do',
'done', 'try', 'many','from', 'subject', 're', 'edu','some', 'nice', 'thank',
'think', 'see', 'rather', 'easy', 'easily', 'lot', 'line', 'even', 'also', 'may', 'take',
'come','using','used','one','two','set','given'])


def limpia_signos(texto):
    return re.sub('[\.,\\\/#¡!¿?$%\^&\*;:{}\[\]=\'+\-_`~()”“"…<>]', ' ', texto).lower().replace('  ',' ')

def limpia_stopwords(texts):
    return [[word for word in simple_preprocess(str(doc)) if word not in stop_words] for doc in texts]

def get_data_words(texto):
    return gensim.utils.simple_preprocess(texto, deacc=True)

def modelo_lda(data_words):
    # Create Dictionary
    id2word = corpora.Dictionary(data_words)
    # Create Corpus
    texts = data_words
    # Term Document Frequency
    corpus = [id2word.doc2bow(text) for text in texts]
    # Build LDA model
    return  gensim.models.LdaMulticore(corpus=corpus,
                                           id2word=id2word,
                                           num_topics=1)


def get(texto_completo):
    try:
        #Limpia texto de signos
        texto_completo = limpia_signos(texto_completo)
        # Genera estructura de palabras
        data_words = get_data_words(texto_completo)
        # Elimina stopwords
        data_words = limpia_stopwords(data_words)
        #Genera modelo LDA
        lda = modelo_lda(data_words)

    except Exception as e:
        return {'ok': False, 'code': 500, 'msj': 'ERROR (topic_modeling.start)', 'error': str(e)}
    return {'ok': True, 'data':
        {
         'topic': str(lda.print_topic(0).replace('"',''))
         }}

