import os
from models import db, User,LoginForm
from config import Configs
from flask_wtf import CSRFProtect
from flask_migrate import Migrate 
from itsdangerous import URLSafeTimedSerializer
from flask_mail import Mail, Message 
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, render_template, request,jsonify,redirect, url_for,session
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity,set_access_cookies



app = Flask(__name__)
serializer = Configs.init_serializer()
app.config.from_object(Configs)

db.init_app(app)
mail = Mail(app)
jwt = JWTManager(app)
csrf = CSRFProtect(app)
migrate = Migrate(app, db)

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
            
            access_token = create_access_token(identity=user.id)
            response = jsonify({'message': 'successfully', 'token':access_token})
            set_access_cookies(response,access_token)
            # session['jwt_token'] = access_token
            return response, 200
        else:
            if request.is_json:
                return jsonify({'error': 'Invalid username or password'}), 401
            else:
                return render_template('login.html', form=form, error='Invalid username or password')

    if request.is_json:
        return jsonify({'error': 'Form validation failed'}), 400
    return render_template('login.html', form=form)


@app.route('/reset-password/<token>', methods=['POST'])
def reset_password(token):
    try:
        username = serializer.loads(token, salt='password-reset-salt', max_age=3600)  # Token valid for 1 hour
    except Exception as e:
        return jsonify({'message': 'The token is invalid or has expired.'}), 400

    data = request.get_json()
    new_password = data.get('password')
    user = User.query.filter_by(username=username).first()
    if user and user.reset_token == token:
        user.password = generate_password_hash(new_password)
        user.reset_token = None 
        db.session.commit()
        return jsonify({'message': 'Password has been reset successfully.'}), 200
    else:
        return jsonify({'message': 'Invalid token or user not found.'}), 400


@app.route('/forgot-password', methods=['POST'])
def forgot_password():
    data = request.get_json()
    username = data.get('username')
    user = User.query.filter_by(username=username).first()
    if user:
        token = serializer.dumps(username, salt='password-reset-salt')
        user.reset_token = token
        db.session.commit()
        return jsonify({'message': 'Password reset token generated.', 'token': token}), 200
    else:
        return jsonify({'message': 'User not found.'}), 404


@app.route('/upload', methods=['POST', 'GET'])
@jwt_required() 
def upload_image():
    if request.method == 'POST':
        if 'image' not in request.files:
            return jsonify({'error': 'No file part in the request'}), 400
        image = request.files['image']
        if image.filename == '':
            return jsonify({'error': 'No file selected for uploading'}), 400
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
        image.save(file_path)
        return jsonify({'message': 'Image uploaded successfully'}), 200
    else:
        return render_template('form.html')


if __name__ == '__main__': 
    with app.app_context():
        db.create_all()
    app.run(debug=True)
