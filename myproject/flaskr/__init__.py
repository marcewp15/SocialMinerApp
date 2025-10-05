import os

from flask import (
    Flask, redirect, url_for, session , render_template
)

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )
    
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    #Ruta inicial - redirige al blueprint
    @app.route('/home')
    def index():
        return redirect(url_for('home.index'))

    #Registra/importa blueprint
    from . import home
    app.register_blueprint(home.bp)
    
    #Manejo de errores app con codigos de estado
    #Página no encontrada - Manejo de error 404
    @app.errorhandler(404) 
    def pagina_no_encontrada(e):
        return render_template("error.html", mensaje="La página no está disponible", codigo=404), 404
    
    #Aplicación no disponible/error de servicio - Manejo de error 500
    @app.errorhandler(500) 
    def error_servidor(e):
        return render_template("error.html", mensaje="La aplicación no está disponible en este momento.",codigo=500), 500
    
    #Servidor no disponible - Manejo de error 503
    @app.errorhandler(503)
    def servidor_no_disponible(e):
        return render_template("error.html", mensaje="La aplicación no está disponible en este momento.",codigo=503), 503
    
    return app