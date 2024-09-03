import os
from models import db, User,LoginForm
from config import settings
from flask_wtf import CSRFProtect
from flask_migrate import Migrate  
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, render_template, request,jsonify,redirect, url_for,session
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity




app = Flask(__name__)
app.config['SECRET_KEY'] = settings.secret_key
app.config['UPLOAD_FOLDER'] = os.path.join('uploads')
app.config['SQLALCHEMY_DATABASE_URI'] = settings.database_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_TOKEN'] = settings.jwt_token


db.init_app(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)
csrf = CSRFProtect(app) 

# @app.before_first_request
# def create_tables():
#     db.create_all()

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        if request.content_type != 'application/json':
            return jsonify({'message': 'Content-Type must be application/json'}), 415

        data = request.get_json()
        if not data:
            return jsonify({'message': 'Invalid JSON data'}), 400

        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return jsonify({'error': 'Username,  and password are required'}), 400

        if User.query.filter_by(username=username).first():
            return jsonify({'message': 'User already exists'}), 400

        hashed_password = generate_password_hash(password)

        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'User registered successfully'}), 201

    else:
        return render_template('register.html')



@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            # Login successful, create JWT token
            access_token = create_access_token(identity=user.id)
            session['jwt_token'] = access_token
            return redirect(url_for('upload_image'))
        else:
            return jsonify({'error': 'Invalid username or password'}), 401

    return render_template('login.html', form=form)


@app.route('/upload', methods = ['POST', 'GET'])
@jwt_required()
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