from flask import Flask, url_for, redirect, request, render_template
from flask_login import LoginManager, current_user, login_required,login_user
import json

def loadusers():
    return json.load(open('users.json', 'r'))

def save_users(users):
    json.dump(users, open('users.json', 'w'))


app = Flask(__name__)
app.secret_key = '123'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

users = loadusers()


class user:
    def __init__(self, username, password, active=True):
        self.username = username
        self.password = password
        self.active = active

    def is_authenticated(self):
        return True
    
    def is_active(self):
        return self.active

    def is_anonymous(self):
        return False
    
    def get_id(self):
        return str(self.username)
    
@login_manager.user_loader 
def load_user(username):
    currentUser = users.get(username)
    
    if currentUser:
        return user(username, currentUser['password'], currentUser.get('active', True))
    else: return None


#routes
@app.route('/')
@login_required
def hello():
    #f not current_user.is_authenticated:
    #    return redirect(url_for('login'))
    
    return f'Hello, {current_user.get_id()}!'


@app.route('/login', methods=['GET', 'POST'])

def login():
    if current_user.is_authenticated:
        return redirect(url_for('hello'))
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = load_user(username)
        if user and user.password==password and user.active:
            login_user(user)
            return redirect(url_for('hello'))
        elif not user: return render_template('wrongUsernameLogin.html')
        elif not user.password==password: return render_template('wrongPasswordLogin.html')
    else:
        return render_template('login.html')



if __name__ == '__main__':
    app.run(debug=True)
