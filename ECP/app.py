from flask import Flask, render_template, request, jsonify
from database_manager import DatabaseManager

app = Flask(__name__)
db_manager = DatabaseManager()

@app.route('/')
def index():
    users = db_manager.get_all_users()
    return render_template('users.html', users=users)

@app.route('/logins')
def view_logins():
    logins = db_manager.get_all_logins()
    return render_template('logins.html', logins=logins)


@app.route('/api/authenticate', methods=['POST'])
def authenticate():
    data = request.get_json()
    name = data.get('name')
    password = data.get('password')
    if not name or not password:
        return jsonify({"success": False, "message": "Имя и пароль обязательны."}), 400
    ip_address = request.remote_addr
    authenticated = db_manager.authenticate_user(name, password, ip_address)
    if authenticated:
        return jsonify({"success": True, "message": "Аутентификация успешна."}), 200
    else:
        return jsonify({"success": False, "message": "Неверное имя или пароль."}), 401

if __name__ == '__main__':
    app.run(debug=True)
