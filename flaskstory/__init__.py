import os
from flask import Flask
#The top of every python file we import the items it needs to run. In this case we are importing python’s ‘os’ library which will access the host’s os directories and of course import the Flask class from the flask module. (classes always have uppercase first letter)

#define the create_app function
def create_app(test_config=None):
	#create the flask app with information about it’s name and where the “instance” folder is living.
    app = Flask(__name__, instance_relative_config=True)
    # __name__ basis this on the folder name we just made, # # #instance_relative_config=True says configuration files are relative to the instance folder which flask automatically sets to storyapp/instance
	#sets defaults. In this case the secret key which we’ll change before publishing
    app.config.from_mapping(
            SECRET_KEY='dev',
            DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite')
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)
#check to make sure app has access to create a file in the instance folder
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    #quick hello world to make sure things are running
    #route sets the url
    @app.route('/hello')
    def hello():
        return 'Hello, Story World!'

    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')

    return app
