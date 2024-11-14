from flask import Flask, request, jsonify, render_template
from flask_mysqldb import MySQL
from utils import *
import os
import ujson

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'user'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'mydb'
mysql = MySQL(app)

suffer, hash = generate_hash()

@app.before_request
def check_session():
    if request.path.startswith('/static'):
        return
    
    if (not os.environ.get("test_mod") == 'on') and (not request.path == '/'):
        global hash
        global suffer
        code = request.form.get("code")
        if (hash == None) or (suffer == None) or (code == None):
            return jsonify({'error': 'Missing pow'}), 403
        
        if not check_pow(suffer, hash, code):
            return jsonify({'error': 'code invalid'}), 403
        else:
            suffer, hash = generate_hash()

@app.route('/update', methods=['POST'])
def update():
    username = request.form.get('username')
    email = request.form.get('email')

    if (not username) or (not email):
        return jsonify({'error': 'Missing parameter'}), 400

    username = username.replace("'", "\\'")
    email = email.replace("'", "\\'")
    if sql_waf(username) or sql_waf(email):
        return jsonify({'error': 'baned'}), 400
    
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM user WHERE username = '{}'".format(username))
        user = cur.fetchone()

        if user:
            cur.execute("UPDATE user SET email = %s WHERE username = %s", (email, username))
            mysql.connection.commit()
            return jsonify({"message": "User updated successfully"}), 200
        else:
            cur.execute("INSERT INTO user (username, email) VALUES (%s, %s)", (username, email))
            mysql.connection.commit()
            return jsonify({"message": "User added successfully"}), 200
    except Exception as e:
        return jsonify({'error': str(e)})
    finally:
        cur.close()

@app.route('/dump', methods=['POST'])
def dump():    
    path = request.form.get('path')   # todo : Cache when the amount of data is too large
    username = request.form.get('username')
    if not path:
        return jsonify({'error': 'Missing dir parameter'}), 400
    
    try:
        realpath = getdir(path)
        if not realpath:
            return jsonify({"error" : "baned"}), 400
        if os.path.exists(realpath):
            return jsonify({"error" : "dir exists"}), 400
        
        os.mkdir(realpath)
        
        cur = mysql.connection.cursor()
        cur.execute("SELECT email FROM user WHERE username = %s", (username,))
        result = cur.fetchone()

        dumped = ''
        if result:
            user = []
            user.append({unicode_decode(username) : result[0]})
            dumped = ujson.dumps(user)
            # log(dumped)
        else:
            return jsonify({"error" : "no such user"}), 400
    except Exception as e:
        os.rmdir(realpath)
        return jsonify({'error': str(e)}), 400
    
    os.rmdir(realpath)
    return dumped

@app.route('/', methods=['GET'])
def index():
    global suffer
    global hash

    return render_template('index.html', suffer=suffer, hash=hash)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=3000)