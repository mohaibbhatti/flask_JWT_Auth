import os
from flask import Flask, render_template, request,jsonify,redirect, url_for
from flask_wtf import CSRFProtect

from config import settings
from models import db, User


app = Flask(__name__)
app.config['SECRET_KEY'] = settings.secret_key
app.config['UPLOAD_FOLDER'] = os.path.join('uploads')
app.config['SQLALCHEMY_DATABASE_URI'] = settings.database_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db.init_app(app)
csrf = CSRFProtect(app) 

# @app.before_first_request
# def create_tables():
#     db.create_all()

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])


@app.route('/register', methods=['POST', 'GET'])
def register_user():
    if request.method == 'POST':
        if request.content_type != 'application/json':
            return jsonify({'message': 'Content-Type must be application/json'}), 415

        data = request.get_json()
        if not data:
            return jsonify({'message': 'Invalid JSON data'}), 400

        name = data.get('name')
        password = data.get('password')
        if User.query.filter_by(name=name).first():
            return jsonify({'message': 'User already exists'}), 400

        new_user = User(name, password)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message' : "successfully"})
    
    else:
        return render_template('register.html')


@app.route('/login', methods=['POST', 'GET'])
def login_user():
    if request.method == 'POST':
        if request.content_type != 'application/json':
            return jsonify({'message': 'Content-Type must be application/json'}), 415

        data = request.get_json()
        if not data:
            return jsonify({'message': 'Invalid JSON data'}), 400

        name = data.get('name')
        password = data.get('password')
        user = User.query.filter_by(name=name).first()
        

        if not user or user.password != password:
            return jsonify({'message': 'Invalid credentials'}), 401

        return jsonify({'message': 'User logged in successfully'})
    
    else:
        return render_template('login.html')


@app.route('/upload', methods = ['POST', 'GET'])

def upload_image( ):
    if request.method == 'POST':
        image = request.files['image']
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
        image.save(file_path)
        return jsonify({'message': 'Image uploaded successfully'})
    else:
        return render_template('form.html')


if __name__ == '__main__': 
    with app.app_context():
        db.create_all()
    app.run(debug=True)