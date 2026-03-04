from flask import Flask, request, jsonify

app = Flask(__name__)

# "База даних" у вигляді списку
users = []
next_id = 1

# Ендпоінт для отримання списку всіх користувачів (GET /users)
@app.route('/users', methods=['GET'])
def get_users():
    return jsonify({
        "status": "ok",
        "data": users,
        "message": "Список користувачів успішно отримано"
    }), 200

# Ендпоінт для створення нового користувача (POST /users)
@app.route('/users', methods=['POST'])
def create_user():
    global next_id
    data = request.get_json()

    if not data or 'name' not in data:
        return jsonify({
            "status": "error",
            "data": None,
            "message": "Не вказано обов'язкове поле 'name'"
        }), 400

    new_user = {
        "id": next_id,
        "name": data['name']
    }
    users.append(new_user)
    next_id += 1
    return jsonify({
        "status": "ok",
        "data": new_user,
        "message": "Користувача успішно створено"
    }), 201

# Ендпоінт для отримання користувача за ID (GET /users/<id>)
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = next((u for u in users if u['id'] == user_id), None)
    if user:
        return jsonify({
            "status": "ok",
            "data": user,
            "message": "Користувача знайдено"
        }), 200
    else:
        return jsonify({
            "status": "error",
            "data": None,
            "message": "Користувача не знайдено"
        }), 404

# Ендпоінт для оновлення користувача (PUT /users/<id>)
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    user = next((u for u in users if u['id'] == user_id), None)
    if user and data and 'name' in data:
        user['name'] = data['name']
        return jsonify({
            "status": "ok",
            "data": user,
            "message": "Користувача оновлено"
        }), 200
    elif not user:
        return jsonify({"status": "error", "data": None, "message": "Користувача не знайдено"}), 404
    else:
        return jsonify({"status": "error", "data": None, "message": "Некоректні дані"}), 400

# Ендпоінт для видалення користувача (DELETE /users/<id>)
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    global users
    user = next((u for u in users if u['id'] == user_id), None)
    if user:
        users = [u for u in users if u['id'] != user_id]
        return jsonify({
            "status": "ok",
            "data": user,
            "message": "Користувача видалено"
        }), 200
    else:
        return jsonify({
            "status": "error",
            "data": None,
            "message": "Користувача не знайдено"
        }), 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)