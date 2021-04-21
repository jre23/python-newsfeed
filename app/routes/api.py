from flask import Blueprint, request, jsonify, session
from app.models import User
from app.db import get_db
import sys

bp = Blueprint('api', __name__, url_prefix='/api')

@bp.route('/users', methods=['POST'])
def signup():
  data = request.get_json()
  db = get_db()

  # create a new user
  # python dict so have to use bracket notation
  try:
    newUser = User(
      username = data['username'],
      email = data['email'],
      password = data['password']
    )

    # save to database
    db.add(newUser)
    db.commit()
  except:
    # newUser addition failed so send an error message to front end
    print(sys.exc_info()[0], 'Signup error')

    # failed so rollback
    db.rollback()
    # clear any existing session data and create two new session properties to keep track of a user's logged in status
    session.clear()
    session['user_id'] = newUser.id
    session['loggedIn'] = True
    return jsonify(message = 'Signup failed'), 500

  return jsonify(id = newUser.id)

@bp.route('/users/logout', methods=['POST'])
def logout():
  # remove session variables
  session.clear()
  return '', 204

@bp.route('/users/login', methods=['POST'])
def login():
    data = request.get_json()
    db = get_db()
    
    try:
      user = db.query(User).filter(User.email == data['email']).one()
    except:
      print(sys.exc_info()[0])

      if user.verify_password(data['password']) == False:
        return jsonify(message = 'Incorrect credentials'), 400
        
    session.clear()
    session['user_id'] = user.id
    session['loggedIn'] = True

    return jsonify(id = user.id)
