from flask import Blueprint, render_template

# bp object to consolidate routes using Blueprint(). corresponds to Router middleware of Express.js
bp = Blueprint('home', __name__, url_prefix='/')

# @bp.route() decorator. function returns the route response. render_template to use Jinja2 templates
@bp.route('/')
def index():
  return render_template('homepage.html')

@bp.route('/login')
def login():
  return render_template('login.html')

# <id> parameter
@bp.route('/post/<id>')
def single(id):
  return render_template('single-post.html')