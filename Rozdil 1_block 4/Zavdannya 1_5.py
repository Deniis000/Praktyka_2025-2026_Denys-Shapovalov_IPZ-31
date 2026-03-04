from flask import Flask, request, jsonify
from flask_bcrypt import Bcrypt
import jwt
import datetime
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ваш-надійний-секретний-ключ-для-jwt'
bcrypt = Bcrypt(app)

users_db = {
    "alice": {
        "username": "alice",
        "password": bcrypt.generate_password_hash("password123").decode('utf-8')
    }
}

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            parts = auth_header.split()
            if len(parts) == 2 and parts[0] == 'Bearer':
                token = parts[1]

        if not token:
            return jsonify({'message': 'Токен відсутній!'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = data['username']
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Термін дії токена закінчився!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Невірний токен!'}), 401

        return f(current_user, *args, **kwargs)
    return decorated

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'message': 'Необхідно вказати username та password'}), 400

    username = data['username']
    password = data['password']

    user = users_db.get(username)
    if not user or not bcrypt.check_password_hash(user['password'], password):
        return jsonify({'message': 'Невірне ім\'я користувача або пароль'}), 401

    token = jwt.encode({
        'username': username,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    }, app.config['SECRET_KEY'], algorithm="HS256")

    return jsonify({'token': token}), 200

@app.route('/profile', methods=['GET'])
@token_required
def profile(current_user):
    return jsonify({
        'message': f'Ласкаво просимо, {current_user}!',
        'user_data': {
            'username': current_user,
            'message': 'Це ваш профіль'
        }
    }), 200

if __name__ == '__main__':
    app.run(debug=True)