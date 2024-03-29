import psycopg2, psycopg2.extras
from computing_codes.settings import DSN, MUNGE_FACTOR, UPLOAD_BASEDIR

from flask import g, url_for
from werkzeug.utils import secure_filename

psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)

import bcrypt
import random

import datetime

import os

def connect():
    conn = psycopg2.connect(DSN)
    conn.set_client_encoding('UTF8')
    
    return conn
    
def get_user(email, password_plaintext):
    
    curs = g.db_conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    query = """SELECT user_id, email_address, forename, surname, password_hash, account_type, account_status
               FROM users
               WHERE email_address LIKE %s;
    """
    
    curs.execute(query, (email, ))
    r = curs.fetchone()
    
    if r:
        if r['account_status'] == 'enabled':
            if bcrypt.checkpw(password_plaintext.encode('utf-8'), r['password_hash'].encode('utf-8')):
                user = dict(r)
                del user['password_hash']
                return user
            else:
                #flash failure
                pass
        else:
            #flash failure
            pass
    return False
    
def save_new_project(owner_id, title, description):

    curs = g.db_conn.cursor()
    
    query = """INSERT INTO projects (owner_id, title, description)
               VALUES (%s, %s, %s)
               RETURNING generate_join_code(project_id) as project_code;
    """
    
    curs.execute(query, (owner_id, title, description))
    
    project_code = curs.fetchone()[0]
    g.db_conn.commit()
    
    return project_code
    
def join_project(user_id, project_code):
    curs = g.db_conn.cursor()
    
    query = """INSERT INTO project_members (project_id, user_id)
               VALUES (decode_join_code(%s), %s)
               RETURNING generate_join_code(project_id) as project_code;
    """
    
    curs.execute(query, (project_code, user_id))
    
    project_code = curs.fetchone()[0]
    g.db_conn.commit()
    
    return project_code
    
def get_projects(user_id):
    curs = g.db_conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    query = """SELECT p.project_id, generate_join_code(p.project_id) as project_code, title, description
               FROM projects p
               LEFT JOIN project_members m ON m.project_id=p.project_id
               WHERE (p.owner_id = %(user_id)s
               OR m.user_id = %(user_id)s)
               AND not p.deleted;
    """
    
    curs.execute(query, {'user_id': user_id})
    r = curs.fetchall()
    
    return r
    
def get_project_details(project_code):
    curs = g.db_conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    query = """SELECT p.project_id, generate_join_code(p.project_id) as project_code, title, description, owner_id
               FROM projects p
               WHERE p.project_id = decode_join_code(%s)
               AND not p.deleted;
    """
    
    curs.execute(query, (project_code, ))
    r = curs.fetchone()
    
    return r
    
def save_uploaded_file(user_id, project_code, file):
    filename = secure_filename(file.filename)
    
    curs = g.db_conn.cursor()
    
    query = """INSERT INTO notes (owner_id, project_id, content, style)
               VALUES (%s, decode_join_code(%s), %s, 'file')
               RETURNING note_id;
    """
    
    curs.execute(query, (user_id, project_code, filename))
    
    note_id = curs.fetchone()[0]
    g.db_conn.commit()
    
    file.save(os.path.join(UPLOAD_BASEDIR, str(user_id), str(note_id), filename))
    
    return note_id