from flask import Flask
from app.routes import home, dashboard, api
from app.db import init_db
from app.utils import filters

def create_app(test_config=None):
  # app config
  app = Flask(__name__, static_url_path='/') # serve any static resources from the root directory
  app.url_map.strict_slashes = False # trailing slashes are optional (/dashboard == /dashboard/)
  app.config.from_mapping(
    SECRET_KEY="super_secret_key" # used when creating server-side sessions
  )

  # decorator
  @app.route('/hello')
  def hello():
    return 'hello world'
  
  # register routes
  app.register_blueprint(home)
  app.register_blueprint(dashboard)
  app.register_blueprint(api)

  # calls Base.metadata.create_all(engine) to create database connection. Base = declarative_base().
  init_db(app)

  # register filters with jinja template environment
  app.jinja_env.filters['format_date'] = filters.format_date
  app.jinja_env.filters['format_url'] = filters.format_url
  app.jinja_env.filters['format_plural'] = filters.format_plural
  
  return app