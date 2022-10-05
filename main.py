from flask import Flask, request
from flask import render_template

import sqlite3

app = Flask(__name__, template_folder='./templates', static_folder='./static')

def init():
    connection = sqlite3.connect('./data/db.sqlite')
    cursor = connection.cursor()

    cursor.execute('CREATE TABLE IF NOT EXISTS users (username, password)')
    
    connection.commit()
    connection.close()


@app.route('/')
def index():
    init()
    
    user = 'гость'
    context = {'user': user}

    return render_template('index.html', **context)


@app.route('/login/', methods=['GET', 'POST'])
@app.route('/login/<username>/<password>/')

def login():
    context = {'error': ''}
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        connection = sqlite3.connect('./data/db.sqlite')
        fetcher = connection.cursor()

        fetcher.execute('SELECT * FROM \'users\' WHERE username = ?', (username,))

        all = fetcher.fetchall()
        connection.close()

        if not (username, password) in all:
            context = {'error': 'Неправильный логин или пароль.'}
            return render_template('login.html', **context)
        else:
            context = {'user': username}
            return render_template('index.html', **context)
    else:
        return render_template('login.html', **context)


@app.route('/register/', methods=['GET', 'POST'])
@app.route('/register/<username>/<password>/')

def register():
    context = {'error': ''}
    
    if request.method == 'POST':
        usernames = []

        new_username = request.form.get('username')
        new_password = request.form.get('password')

        connection = sqlite3.connect('./data/db.sqlite')
        
        fetcher = connection.cursor()
        setter = connection.cursor()

        fetcher.execute('SELECT * FROM \'users\'')
        
        all = fetcher.fetchall()

        for name, password in all:
            usernames.append(name)
        
        if new_username in usernames:
            context = {'error': 'Данное имя пользователя уже занято.'}
            return render_template('register.html', **context)
    
        setter.execute('INSERT INTO \'users\' VALUES (?, ?)', (new_username, new_password))
        
        connection.commit()
        connection.close()

        return '<h1>Аккаунт зарегестрирован успешно!</h1>'
    else:
        return render_template('register.html', **context)


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html')


if __name__ == '__main__':
    app.run()
