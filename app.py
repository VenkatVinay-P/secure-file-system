from flask import Flask, render_template, redirect, url_for, request, send_file,flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from cryptography.fernet import Fernet
#from app import db
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = b'V\x98\xb0\xbfnj\xd7\xfd\x12\xb5\xcb\xb4A\x9cm\xda\xf0\xd4\\\xe7\xf5\x9a\x85\xf0'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

# Generate and save the key
if not os.path.exists('secret.key'):
    with open('secret.key', 'wb') as key_file:
        key_file.write(Fernet.generate_key())
with open('secret.key', 'rb') as key_file:
    key = key_file.read()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(50), default='user')

class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(150),nullable=False)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/Signup',methods=['GET','POST'])
def signup():
    if request.method=='POST':
        username=request.form['username']
        password=request.form['password']
        if User.query.filter_by(username=username).first():
            flash('Username already exists')
            return redirect(url_for('Signup'))
        new_user=User(username=username,password=password)
        db.session.add(new_user)
        db.session.commit()
        flash('User created successfully')
        return redirect(url_for('login'))
    return render_template('Signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Invlaid user and pass')
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    files=File.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', username=current_user.username,files=files)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/admin')
@login_required
def admin_dashboard():
    if current_user.role == 'admin':
        return 'Welcome Admin!'
    else:
        return 'Access Denied', 403

@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename=file.filename
            file_path = os.path.join('uploads', filename)
            file.save(file_path)
            encrypt_file(file_path, key)
            new_file=File(filename=filename,user_id=current_user.id)
            db.session.add(new_file)
            db.session.commit()
            print('File uploaded and encrypted successfully!')
            return redirect(url_for('dashboard'))
    return render_template('upload.html')

@app.route('/download/<filename>')
@login_required
def download_file(filename):
    file_path = os.path.join('uploads', filename)
    decrypt_file(file_path, key)
    return send_file(file_path, as_attachment=True)

def encrypt_file(file_path, key):
    fernet = Fernet(key)
    with open(file_path, 'rb') as file:
        original = file.read()
    encrypted = fernet.encrypt(original)
    with open(file_path, 'wb') as encrypted_file:
        encrypted_file.write(encrypted)

def decrypt_file(file_path, key):
    fernet = Fernet(key)
    with open(file_path, 'rb') as encrypted_file:
        encrypted = encrypted_file.read()
    decrypted = fernet.decrypt(encrypted)
    with open(file_path, 'wb') as decrypted_file:
        decrypted_file.write(decrypted)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        if not os.path.exists('uploads'):
            os.makedirs('uploads')
    app.run(debug=True)
