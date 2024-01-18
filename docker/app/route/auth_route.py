from flask import request
import jwt
import bcrypt
from flask import request
from flask_restx import Resource, Namespace, fields

from handlers import Logger

logging = Logger.set_logger(log_name='Server', filename='logs/server.log')

users = {}

Auth = Namespace(
    name="AI",
    description="AI FACE SWAP API",
)

user_fields_auth = Auth.model('User', {  # Model 객체 생성
    'name': fields.String(description='User Name', required=True, example="test"),
    'password': fields.String(description='Password', required=True, example="1234")
})

@Auth.route('/register')
class AuthRegister(Resource):
    @Auth.expect(user_fields_auth)
    @Auth.doc(responses={200: 'Success'})
    @Auth.doc(responses={410: 'Your ID same Registed'})
    def post(self):
        name = request.json['name']
        password = request.json['password']
        logging.info(f"name: {name} password: {password}")
        if name in users:
            logging.error("message: Your ID same Registed")
            return {
                "message": "Your ID same Registed"
            }, 410
        else:
            users[name] = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())  # 비밀번호 저장
            logging.info(f"Token: {users[name]}")
            return {
                'Authorization': jwt.encode({'name': name}, users[name], algorithm="HS256")  # str으로 반환하여 return
            }, 200

@Auth.route('/login')
class AuthLogin(Resource):
    @Auth.expect(user_fields_auth)
    @Auth.doc(responses={200: 'Success'})
    @Auth.doc(responses={411: 'User Not Found'})
    @Auth.doc(responses={412: 'Auth Failed'})
    def post(self):
        name = request.json['name']
        password = request.json['password']
        logging.info(f"name: {name} password: {password}")
        if name not in users:
            logging.error("message: User Not Found")
            return {
                "message": "User Not Found"
            }, 411
        elif not bcrypt.checkpw(password.encode('utf-8'), users[name]):  # 비밀번호 일치 확인
            logging.error("message: User Password wrong")
            return {
                "message": "User Password wrong"
            }, 412
        else:
            return {
                'Authorization': jwt.encode({'name': name}, users[name], algorithm="HS256") # str으로 반환하여 return
            }, 200
