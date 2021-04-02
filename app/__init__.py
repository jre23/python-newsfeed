from flask import Flask
from app.routes import home
from app.routes import dashboard

def create_app(test_config=None):
  # app config
  app = Flask(__name__, static_url_path='/') # serve any static resources from the root directory
  app.url_map.strict_slashes = False # trailing slashes are optional
  app.config.from_mapping(
    SECRET_KEY="super_secret_key" # used when creating server-side sessions
  )

  @app.route('/hello')
  def hello():
    return 'hello world'
  
  # register routes
  app.register_blueprint(home)
  app.register_blueprint(dashboard)

  return app