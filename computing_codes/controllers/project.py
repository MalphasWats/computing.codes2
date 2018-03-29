from flask import Blueprint, render_template, session, redirect, url_for, request
#from computing_codes import public_endpoint

import computing_codes.model as model

mod = Blueprint('project', __name__)

@mod.route('/')
def index():
    #if 'user' in session:
    #    return redirect(url_for('overview.index'))
        
    return "Not Implemented" #render_template('home.html')
    
@mod.route('/create')
def create():
    return render_template('new_project.html')
    
@mod.route('/save_new')
def save_new():
    project_id = 0
    return redirect(url_for('.view_project', project_id))
    
@mod.route('/<int:project_id>/')
def view_project(project_id):
    return "Not Implemented ({})".format(project_id)