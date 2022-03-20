import pymongo, bson
from config import MONGO_URI,BD,COLLECTION


def get_client():
    try:
        c = pymongo.MongoClient(MONGO_URI)
    except Exception as e:
        raise Exception('(database.get_client)' + str(e))
    return c


def get(filtros, lista_variables=None):
    client = None
    try:
        client = get_client()
        if filtros:
            if '_id' in filtros: filtros['_id'] = bson.objectid.ObjectId(filtros['_id'])
        res = client[BD][COLLECTION].find(filtros,lista_variables)
        l=[]
        for r in res: l.append(r)
    except Exception as e:
        raise Exception('(database.get)' + str(e))
    finally:
        if client: client.close()
    return l


def save(document):
    client = None
    try:
        client = get_client()
        res = client[BD][COLLECTION].insert_one(document)
    except Exception as e:
        raise Exception('(database.save)' + str(e))
    finally:
        if client: client.close()
    return res

def update_many(documents):
    client = None
    try:
        client = get_client()
        res = client[BD][COLLECTION].update_many(documents)
    except Exception as e:
        raise Exception('(database.update_many)' + str(e))
    finally:
        if client: client.close()
    return res

def update_one(document,new_date):
    client = None
    try:
        client = get_client()
        res = client[BD][COLLECTION].update_one(document,{'$set':new_date})
    except Exception as e:
        raise Exception('(database.update_one)' + str(e))
    finally:
        if client: client.close()
    return res


def delete_many_by_ids(ids):
    client = None
    try:
        client = get_client()
        res = client[BD][COLLECTION].delete_many({'_id':{'$in':ids}})
    except Exception as e:
        raise Exception('(database.update_many)' + str(e))
    finally:
        if client: client.close()
    return res

