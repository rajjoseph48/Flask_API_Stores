from flask_restful import Resource
from flask_jwt import jwt_required
from models.store import StoreModel

class StoreList(Resource):
    def get(self):
        stores = list(map(lambda x:x.json(), StoreModel.query.all()))
        return {'stores':stores}


class Store(Resource):

    def get(self,name):
        store = StoreModel.get_store_by_name(name)
        if store:
            return store.json()
        else:
            return {'Message': 'store not found'}, 404

    def post(self,name):

        if StoreModel.get_store_by_name(name):
            return {'Message': 'Store with name {} already exists'.format(name)}, 400
            
        store = StoreModel(name)

        try:
            store.save_to_db()
        except:
            return  {'Message': 'An error occured while creating item'}, 500

        return store.json(), 201

    def delete(self,name):
        store = StoreModel.get_store_by_name(name)

        if store:
            store.del_from_db()
            return {'Message': 'Store deleted'}
        return {'Message': 'Store named {} does not exists'.format(name)}, 404
