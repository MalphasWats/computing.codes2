from flask import Blueprint, render_template, session, redirect, url_for, request, flash
#from computing_codes import public_endpoint

import computing_codes.model as model

mod = Blueprint('note', __name__)

@mod.route('/')
def index():
    return "Not Implemented"
    
@mod.route('/upload', methods=['POST'])
def upload():
    
    project_code = request.form.get('project_code')
    file = request.files['file']
    
    if request.files['file'].filename != '':
        model.save_uploaded_file(session['user']['user_id'], project_code, file)
    
    return redirect(url_for('project.view_project', project_code=project_code))
    