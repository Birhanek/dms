from flask import Blueprint, request,jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, current_user, login_required
# Local imports
from .models import User
from . import session
from checker import check_string

auth = Blueprint('auth',__name__)

@auth.route('/signup',methods=['GET','POST'])
def signUp():
    if request.method == 'POST':
        first_name = request.form.get('firstName')
        last_name = request.form.get('lastName')
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role')
        print(email)

        print(role)

        user = session.query(User).filter_by(email=email).first()
        if user:
            return jsonify({
                "ërror": " User already existed! Please login"
            })
        else:
            if not '@' in email and not '.' in email:
                return jsonify({
                    "error": "email is not correct!"
                })
            elif len(first_name) < 2 or len(last_name) < 2:
                return jsonify({
                    "error": "Either first name or last name is too short. "
                })
            elif len(password) < 7 or not check_string(password):
                return jsonify({
                    "error": "either the password is less than 7 character."
                })
            else:
                new_user = User(
                    first_name = first_name,
                    last_name = last_name,
                    email = email,
                    password = generate_password_hash(password),
                    role = role,
                    last_login = None
                )

                # Add the new User instance to the session
                session.add(new_user)

                # Commit the session to save the new user to the database
                session.commit()

    return jsonify({'message': 'File uploaded successfully'}),201

# An endpoint used to login  
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if not email or not password:
            return jsonify({
                "error": "Either email or password is not provided!"
            })
        else:
            user = session.query(User).filter_by(email=email).first()
      
            if not user:
                return jsonify({
                    "error": "user does not existed, please signup!"
                })
            else:
                if check_password_hash(user.password, password):
                    login_user(user,remember=True)

                    return jsonify({
                        "message": "user logged in successfully"
                    })
                else:
                    return jsonify({
                        "error": "Password or email is incorrect!"
                    })

# An endpoint user to logout from the system
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return jsonify({
        "message": "user successfully loggedout!"
    })
