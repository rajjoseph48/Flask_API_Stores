from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

class Items(Resource):
    def get(self):
        items = list(map(lambda x:x.json(), ItemModel.query.all()))
        return {'items':items}


class Item(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('price',
            type = float,
            required = True,
            help="This field cannot be left blank!"
        )
    parser.add_argument('store_id',
            type = float,
            required = True,
            help="Every Items must contain a store id"
        )

    @jwt_required()
    def get(self,name):
        item = ItemModel.get_item_by_name(name)
        if item:
            return item.json()
        else:
            return {'Message': 'item not found'}, 404

    def post(self,name):

        if ItemModel.get_item_by_name(name):
            return {'Message': 'Item already exists'}, 400

        data = Item.parser.parse_args()
        item = ItemModel(name, **data)

        try:
            item.save_to_db()
        except:
            return  {'Message': f'An error occured while creating item'}, 500

        return item.json(), 201

    def delete(self,name):
        item = ItemModel.get_item_by_name(name)

        if item:
            item.del_from_db()
            return {'Message': 'Item deleted'}
        return {'Message': 'Item does not exists'}, 404

    def put(self,name):

        data = Item.parser.parse_args()
        item = ItemModel.get_item_by_name(name)

        if item:
            item.price = data['price']
            item.store_id = data['store_id']
        else:
            item = ItemModel(name, **data)

        item.save_to_db()
        return item.json()
