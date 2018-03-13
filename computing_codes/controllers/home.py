from flask import Blueprint, render_template, session, redirect, url_for
from computing_codes import public_endpoint

mod = Blueprint('home', __name__)

@mod.route('/')
@public_endpoint
def index():
    #if 'user' in session:
    #    return redirect(url_for('overview.index'))
        
    return render_template('home.html')
    