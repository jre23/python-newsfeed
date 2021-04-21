from flask import Blueprint, render_template, session, redirect
from app.models import Post
from app.db import get_db

# bp object to consolidate routes using Blueprint(). corresponds to Router middleware of Express.js
bp = Blueprint('home', __name__, url_prefix='/')

# @bp.route() decorator. function returns the route response. render_template to use Jinja2 templates
@bp.route('/')
def index():
  # get all posts
  db = get_db()
  posts = (
    db.query(Post).order_by(Post.created_at.desc()).all()
  )
  # render all posts to homepage template
  return render_template(
    'homepage.html',
    posts=posts,
    loggedIn=session.get('loggedIn'))

@bp.route('/login')
def login():
  # if user not already logged in, render login page, else redirect to dashboard
  if session.get('loggedIn') is None:
    return render_template('login.html')

  return redirect('/dashboard')

# <id> parameter
@bp.route('/post/<id>')
def single(id):
  # get single post by id
  db = get_db()
  post = db.query(Post).filter(Post.id == id).one()
  # render single post to single-post template
  return render_template(
    'single-post.html',
    post=post,
    loggedIn=session.get('loggedIn'))