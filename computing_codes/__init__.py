from flask import (Flask, session, request, redirect, url_for, g)

import computing_codes.model

app = Flask(__name__, template_folder='views')
app.config.from_object('computing_codes.settings')


def public_endpoint(function):
    function.is_public = True
    return function
    
    
@app.before_request
def check_valid_login():

    login_valid = 'user' in session
    
    g.db_conn = computing_codes.model.connect()
        
    if (request.endpoint and 
        'static' not in request.endpoint and 
        not login_valid and 
        not getattr(app.view_functions[request.endpoint], 'is_public', False) ) :
        return redirect(url_for('home.index'))
        
        
@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'db_conn'):
        g.db_conn.close()
        
        
import computing_codes.controllers.home
import computing_codes.controllers.project
import computing_codes.controllers.note

app.register_blueprint(computing_codes.controllers.home.mod)
app.register_blueprint(computing_codes.controllers.project.mod, url_prefix='/project')
app.register_blueprint(computing_codes.controllers.note.mod, url_prefix='/note')
