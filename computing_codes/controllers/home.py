from flask import Blueprint, render_template, session, redirect, url_for, request, flash
from computing_codes import public_endpoint

import computing_codes.model as model

mod = Blueprint('home', __name__)

@mod.route('/')
@public_endpoint
def index():
    #if 'user' in session:
    #    return redirect(url_for('overview.index'))
        
    return render_template('home.html')
    
@mod.route('/overview')
def overview():
    projects = model.get_projects(session['user']['user_id'])
    return render_template('overview.html', projects=projects)
    
@mod.route('/login', methods=['GET', 'POST'])
@public_endpoint
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password_plaintext = request.form.get('password')

        user = model.get_user(email, password_plaintext)
        if user:
            session['user'] = user
            return redirect(url_for('home.overview'))
        else:
            flash("Incorrect username or password.", category='error')
        
    return redirect(url_for('home.index'))
    

@mod.route('/logout')
def logout():
    session.pop('user')
    return redirect(url_for('home.index'))
    
