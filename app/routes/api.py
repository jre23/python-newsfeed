from flask import Blueprint, request, jsonify, session
from app.models import User, Post, Comment, Vote
from app.db import get_db
import sys

bp = Blueprint('api', __name__, url_prefix='/api')

# matches with /api/users
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

# matches with /api/users/logout
@bp.route('/users/logout', methods=['POST'])
def logout():
  # remove session variables
  session.clear()
  return '', 204

# matches with /api/users/login
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

# matches with /api/comments
@bp.route('/comments', methods=['POST'])
def comment():
  data = request.get_json()
  db = get_db()

  try:
    # create a new comment. comment_text and post_id come from the front-end. user_id is from the session
    newComment = Comment(
      comment_text = data['comment_text'],
      post_id = data['post_id'],
      user_id = session.get('user_id')      
    )
    db.add(newComment)
    db.commit()
  except:
    print(sys.exc_info()[0], 'Comment failure')

    db.rollback()
    return jsonify(message = 'Comment failed'), 500

  return jsonify(id = newComment.id)

# matches with /api/posts/upvotes
@bp.route('/posts/upvote', methods=['PUT'])
def upvote():
  data = request.get_json()
  db = get_db()

  try:
    newVote = Vote(
      post_id = data['post_id'],
      user_id = session.get('user_id')
    )

    db.add(newVote)
    db.commit()
  except:
    print(sys.exc_info()[0])

    db.rollback()
    return jsonify(message = 'Upvote failed'), 500
  
  return '', 204

  
# @bp.route('/posts', methods=['POST'])
# def post():
#   data = request.get_json()
#   db = get_db()