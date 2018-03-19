from flask import Blueprint, render_template, session, redirect, url_for
from computing_codes import public_endpoint

import lessonpad.model as model

mod = Blueprint('home', __name__)

@mod.route('/')
@public_endpoint
def index():
    #if 'user' in session:
    #    return redirect(url_for('overview.index'))
        
    return render_template('home.html')
    
@mod.route('/overview')
def overview():
    return render_template('overview.html')
    
@mod.route('/login', methods=['GET', 'POST'])
@public_endpoint
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password_plaintext = request.form.get('password')

        user = model.account.get_user(email, password_plaintext)
        if user:
            session['user'] = user
            return redirect(url_for('home.overview'))
        
    return redirect(url_for('home.index'))
    

@mod.route('/logout')
def logout():
    session.pop('user')
    return redirect(url_for('home.index'))
    
