from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import LoginManager, login_user, login_required, current_user, logout_user

# Inicializa o aplicativo Flask
app = Flask(__name__)

# Configura o banco de dados SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key_here'

# Inicializa o SQLAlchemy
db = SQLAlchemy(app)

# Inicializa o Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)

# Criação do modelo User com campos nome e confirm_password
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)  # Campo para nome
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f'<User {self.name}>'

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

# Modelo de Post, com relacionamento com User e data/hora de criação
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(500), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'<Post {self.content[:20]}>'

# Criação das tabelas dentro do contexto de aplicativo
with app.app_context():
    db.create_all()

# Função para carregar o usuário a partir do banco de dados
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    posts = Post.query.all()  # Busca todos os posts
    return render_template('index.html', posts=posts)

# Rota de login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Verifica se o email e senha existem no banco de dados
        user = User.query.filter_by(email=email, password=password).first()

        if user:
            login_user(user)  # Faz o login do usuário
            flash('Login bem-sucedido!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Email ou senha incorretos.', 'error')

    return render_template('login.html')

# Rota de registro
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']  # Novo campo para nome
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']  # Campo de confirmação da senha

        # Verifica se a senha e a confirmação da senha coincidem
        if password != confirm_password:
            flash('As senhas não coincidem.', 'error')
        elif User.query.filter_by(email=email).first():
            flash('Email já registrado.', 'error')
        else:
            # Cria um novo usuário e salva no banco de dados
            new_user = User(name=name, email=email, password=password)
            db.session.add(new_user)
            db.session.commit()
            flash('Usuário registrado com sucesso.', 'success')
            return redirect(url_for('login'))

    return render_template('register.html')

# Rota para criar um novo post (somente usuários autenticados podem criar posts)
@app.route('/post', methods=['POST'])
@login_required
def create_post():
    content = request.form['content']

    if content:
        # Cria o novo post e associa ao usuário
        new_post = Post(content=content, user_id=current_user.id)  # Usa o ID do usuário logado
        db.session.add(new_post)
        db.session.commit()
        flash('Post criado com sucesso!', 'success')

    return redirect(url_for('index'))

# Rota de logout
@app.route('/logout')
@login_required
def logout():
    logout_user()  # Faz o logout do usuário
    flash('Você foi deslogado.', 'success')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
