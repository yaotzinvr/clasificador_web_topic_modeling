import sys, os, pymongo, bson
sys.path.append(os.path.abspath(".."))
from main import MONGO_URI
BD = 'TopicModeling'


def get_client():
    try:
        c = pymongo.MongoClient(MONGO_URI)
    except Exception as e:
        raise Exception('(db.get_client)' + str(e))
    return c


def get(filtros, lista_variables=None, collection = 'articulos'):
    client = None
    try:
        client = get_client()
        if filtros:
            if '_id' in filtros: filtros['_id'] = bson.objectid.ObjectId(filtros['_id'])
        res = client[BD][collection].find(filtros,lista_variables)
        l=[]
        for r in res: l.append(r)
    except Exception as e:
        raise Exception('(db.get)' + str(e))
    finally:
        if client: client.close()
    return l


def save(document, collection = 'articulos'):
    client = None
    try:
        client = get_client()
        res = client[BD][collection].save(document)
    except Exception as e:
        raise Exception('(db.save)' + str(e))
    finally:
        if client: client.close()
    return str(res)

def update_many(documents, collection = 'articulos'):
    client = None
    try:
        client = get_client()
        res = client[BD][collection].update_many(documents)
    except Exception as e:
        raise Exception('(db.update_many)' + str(e))
    finally:
        if client: client.close()
    return str(res)




