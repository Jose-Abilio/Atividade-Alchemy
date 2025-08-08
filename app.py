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
class Usuario(db.Model,UserMixin):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key = True)
    nome = db.Column(db.String(40),nullable = False, unique = True)
    senha = db.Column(db.String(40),nullable = False)


@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        nome = request.form['name']
        senha= request.form['password']

        user =  Usuario.query.filter_by(nome=nome).first()

        if user and check_password_hash(user.senha,senha):
            login_user(user)
            return redirect(url_for('dash'))
        else:
           return redirect(url_for('login'))
        
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nome = request.form['name']
        senha = request.form['password']

        # Verifica se usuário já existe
        if Usuario.query.filter_by(nome=nome).first():
            flash('Nome de usuário já existe.')
            return redirect(url_for('register'))

        # Cria e salva no banco
        senha_hash  = generate_password_hash(senha)
        novo_usuario = Usuario(nome=nome, senha=senha_hash)
        db.session.add(novo_usuario)
        db.session.commit()

        return redirect(url_for('login'))

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