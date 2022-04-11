import pymongo, bson
from config import MONGO_URI,BD,COLLECTION


def get_client():
    try:
        c = pymongo.MongoClient(MONGO_URI)
    except Exception as e:
        raise Exception('(get_client)' + str(e))
    return c


def get(filtros, atributos=None):
    client = None
    try:
        client = get_client()
        print(client[BD][COLLECTION].find())
        if filtros:
            if '_id' in filtros: filtros['_id'] = bson.objectid.ObjectId(filtros['_id'])
        res = client[BD][COLLECTION].find(filtros,atributos)
        l=[]
        for r in res: l.append(r)
    except Exception as e:
        raise Exception('(get)' + str(e))
    finally:
        if client: client.close()
    return l

def save(document):
    client = None
    try:
        client = get_client()
        res = client[BD][COLLECTION].insert_one(document)
    except Exception as e:
        raise Exception('(save)' + str(e))
    finally:
        if client: client.close()
    return res.inserted_id

def delete(_id):
    client = None
    try:
        client = get_client()
        res = client[BD][COLLECTION].delete_one({'_id': bson.objectid.ObjectId(_id)})
    except bson.errors.InvalidId as e:
        print(e)
        raise Exception('ID INVÁLIDO')
    except Exception as e:
        raise Exception('(delete)' + str(e))
    finally:
        if client: client.close()
    return res.deleted_count

def update_many(documents):
    client = None
    try:
        client = get_client()
        res = client[BD][COLLECTION].update_many(documents)
    except Exception as e:
        raise Exception('(update_many)' + str(e))
    finally:
        if client: client.close()
    return res

def update_one(document,new_date):
    client = None
    try:
        client = get_client()
        res = client[BD][COLLECTION].update_one(document,{'$set':new_date})
    except Exception as e:
        raise Exception('(update_one)' + str(e))
    finally:
        if client: client.close()
    return res


def delete_many_by_ids(ids):
    client = None
    try:
        client = get_client()
        res = client[BD][COLLECTION].delete_many({'_id':{'$in':ids}})
    except Exception as e:
        raise Exception('(update_many)' + str(e))
    finally:
        if client: client.close()
    return res.deleted_count

if __name__=='__main__':
    #delete('6236da13c87f5e6139a82c90')
    print(get_client().server_info())
