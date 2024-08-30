from flask import Flask, render_template, redirect, url_for, flash, request, session, jsonify
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
from config import Config
import os
from functools import wraps
from PIL import Image

app = Flask(__name__)
app.config.from_object(Config)
mysql = MySQL(app)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login',error='not_log_yet'))
        return f(*args, **kwargs)
    return decorated_function

@app.route("/")
def main():
    return redirect(url_for('display'))
    # return render_template("index.html",photos=None)

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form.get('email')  # 获取邮箱
        # 使用 pbkdf2:sha256 方法进行密码哈希
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            # flash('Username already exists, please choose another one.','error')
            return redirect(url_for('register', error='username_exists'))

        try:
            cursor.execute(
                "INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s)",
                (username, email, hashed_password)
            )
            mysql.connection.commit()
        except Exception as e:
            # Handle exception or duplicate entries
            return redirect(url_for('register',error='database_error'))
        finally:
            cursor.close()

        return redirect(url_for('login'))

    error = request.args.get('error','')
    print(error)
    return render_template("register.html", error=error)

@app.route("/login", methods=['GET', 'POST'])
def login():
    error = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        try:
            cursor = mysql.connection.cursor()
            cursor.execute("SELECT id, password_hash FROM users WHERE username = %s", (username,))
            user = cursor.fetchone()
            cursor.close()
            # print(user)
            # 检查用户是否存在以及密码是否正确
            if user is None:
                error = "Username does not exist."
            elif not check_password_hash(user[1], password):
                error = "Incorrect password."
            else:
                session['user_id'] = user[0]
                session['username'] = username
                return redirect(url_for('show_photos', user_id=user[0]))
        
        except Exception as e:
            error = str(e)

    return render_template("login.html", error=error)

@app.route("/index/<int:user_id>")
@login_required
def show_photos(user_id):
    if session.get('user_id') != user_id:
        return redirect(url_for('login', error=''))
    # 创建上传目录（如果不存在）
    UPLOAD_FOLDER = f'static/uploads/{user_id}'
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    username = session.get('username', 'Guest')
    # print(username)
    cursor = mysql.connection.cursor()
    # cursor.execute("SELECT filename FROM photos")
    cursor.execute("SELECT filename FROM photos WHERE id = %s", (user_id,))
    photos = cursor.fetchall()
    cursor.close()
    return render_template("index.html",user_id=str(user_id), username=username, photos=photos)

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

@app.route('/index/<int:user_id>/personal_info')
def personal_info(user_id):
    username = session.get('username', 'Guest')
    return render_template('user.html',user_id=user_id, username=username)

@app.route("/upload", methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'success': False, 'error': 'No file part'})
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'success': False, 'error': 'No selected file'})

    # 保存文件和webp文件
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)

    img = Image.open(file_path)
    webp_path = os.path.splitext(file_path)[0] + '.webp'
    img.save(webp_path, 'webp', quality=85)

    # 将文件信息插入数据库
    cursor = mysql.connection.cursor()
    user_id = session.get('user_id', '0')
    cursor.execute("INSERT INTO photos (id, filename) VALUES (%s, %s)", (user_id, file.filename,))
    mysql.connection.commit()
    cursor.close()

    return jsonify({'success': True})

@app.route('/delete_photo', methods=['POST'])
def delete_photo():
    data = request.get_json()
    filename = data.get('filename')

    if not filename:
        return jsonify({'success': False, 'error': 'No filename provided'})

    # 删除数据库中的记录
    cursor = mysql.connection.cursor()
    user_id = session.get('user_id', '0')
    cursor.execute("DELETE FROM photos WHERE id = %s AND filename = %s", (user_id, filename,))
    mysql.connection.commit()

    # 删除文件系统中的文件
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    webp_path = os.path.splitext(file_path)[0] + '.webp'
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            os.remove(webp_path)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

    cursor.close()
    return jsonify({'success': True})


@app.route('/vistor')
def display():
    photos = [file for file in os.listdir('static/displays') if file.endswith(('.jpg','png',))]
    print(photos)
    return render_template("visitor.html",photos=photos)


if __name__ == "__main__":
    app.run(debug=True)