from flask import Flask, render_template
from flask import request, session, redirect, url_for
from flask import flash

from flask_login import LoginManager, UserMixin, logout_user
from flask_login import login_required, login_user, current_user
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
import sqlite3

from flask_sqlalchemy import SQLAlchemy


login_manager = LoginManager()
#inicializando o flask e o alchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.db'
db = SQLAlchemy()
db.init_app(app)
login_manager.__init__(app)

app.secret_key = 'chave_secreta'

#criando as tabelas
class usuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key = True)
    nome = db.Column(db.String(40),nullable = False, unique = True)
    senha = db.Column(db.String(40),nullable = False)

#def obter_conexao():
    #conn = sqlite3.connect('banco.db')
    #conn.row_factory = sqlite3.Row
    #return conn

class User(UserMixin):
    def __init__(self, nome, senha) -> None:
        self.nome = nome
        self.senha = senha

    #@classmethod
    #def get(cls, user_id):
        # user_id nesse caso é um nome
        #conexao = obter_conexao()        
        #sql = "select * from users where nome = ?"
        #resultado = conexao.execute(sql, (user_id,)).fetchone()
        #user = User(nome=resultado['nome'], senha=resultado['senha'])
        #user.id = resultado['nome']
        #return user



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        nome = request.form['name']
        senha= request.form['password']
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nome = request.form['name']
        senha= request.form['password']
        
    return render_template('register.html')


@app.route('/dashboard')
def dash():
    return render_template('dash.html')

@app.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()