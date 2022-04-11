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
    except bson.errors.InvalidId as e:
        print(e)
        raise Exception('ID INVÁLIDO')
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


def update_by_id(id,new_data_field):
    client = None
    try:
        client = get_client()
        res = client[BD][COLLECTION].update_one({'_id':bson.objectid.ObjectId(id)},{'$set':new_data_field})
    except bson.errors.InvalidId as e:
        print(e)
        raise Exception('ID INVÁLIDO')
    except Exception as e:
        raise Exception('(update_by_id)' + str(e))
    finally:
        if client: client.close()
    return res.matched_count



if __name__=='__main__':
    #delete('6236da13c87f5e6139a82c90')
    print(update_by_id('624a63694742c6bd66bf2eeb',{'lda':{'uno':2}}))
    print(get({'_id':'624a63694742c6bd66bf2eeb'},['_id','titulo','lda']))
