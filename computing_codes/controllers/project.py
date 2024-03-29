from flask import Blueprint, render_template, session, redirect, url_for, request, flash
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
    
@mod.route('/save_new', methods=['POST'])
def save_new():
    title = request.form.get('title')
    description = request.form.get('description')
    
    if title == '' or title == 'Title':
        flash("Lessons MUST have a title.", category='error')
        return redirect(url_for('.create'))
    else:
        project_code = model.save_new_project(session['user']['user_id'], title, description)
        return redirect(url_for('.view_project', project_code=project_code))
        
@mod.route('/join', methods=['POST'])
def join():
    project_code = request.form.get('project_code')
    
    if project_code == '' or project_code == 'Project Code':
        return redirect(url_for('home.overview'))
    else:
        project_code = model.join_project(session['user']['user_id'], project_code)
        #TODO: if no project code, redirect with message
        return redirect(url_for('.view_project', project_code=project_code))
    
@mod.route('/<project_code>/')
def view_project(project_code):
    details = model.get_project_details(project_code)
    #TODO: if no details, redirect with message.
    
    if details['owner_id'] == session['user']['user_id']:
        return render_template('project_owner.html', project_details=details)
    else:
        return render_template('project_member.html', project_details=details)