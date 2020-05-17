from flask_restful import Resource, reqparse
from models.user import UserModel

class UserRegister(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument(
            'username',
            required = True,
            type = str,
            help = 'This field can not be empty and must contain a valid username'
        )
    parser.add_argument(
            'password',
            required = True,
            type = str,
            help = 'This field can not be empty and must contain a valid password'
        )

    def post(self):
        data = UserRegister.parser.parse_args()

        user = UserModel.get_user_by_username(data['username'])

        if user:
            return {'Message': f'User already exists. Kindly use a different Username and try again'}, 400
        else:
            #user = UserModel(data['username'],data['password'])
            user = UserModel(**data)

        user.save_to_db()
        return {'Message': f'User created successfully.'}, 201

class Users(Resource):

    def get(self):
        users = list(map(lambda x: x.json(), UserModel.query.all()))
        return {'users':users}
