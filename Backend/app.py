from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import jwt
import datetime
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
CORS(app)  

# Veritabanı
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'supersecretkey'
db = SQLAlchemy(app)

# Entity
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

#Token oluşturulan yer
def generate_token(user_id):
    payload = {
        'user_id': user_id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }
    return jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')

# Kayıt edilen yer
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    
    hashed_password = generate_password_hash(data['password'])
    
    
    new_user = User(
        username=data['username'], 
        password=hashed_password
    )
    
    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'Kullanıcı oluşturuldu!'}), 201
    except:
        return jsonify({'message': 'Kullanıcı zaten var!'}), 409

# Giriş yapılan yer
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()

    if not user or not check_password_hash(user.password, data['password']):
        return jsonify({'message': 'Geçersiz kullanıcı adı veya şifre!'}), 401

    token = generate_token(user.id)
    return jsonify({'token': token})

# token ile girilecek yer
@app.route('/protected', methods=['GET'])
def protected():
    token = request.headers.get('Authorization')
    try:
        data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        user = User.query.get(data['user_id'])
        return jsonify({'message': f'Hoş geldin {user.username}!'})
    except:
        return jsonify({'message': 'Geçersiz token!'}), 401

# Veritabanı oluşturulan yer
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)