import psycopg2, psycopg2.extras
from computing_codes.settings import DSN, MUNGE_FACTOR

from flask import g, url_for

psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)

import bcrypt
import random

import datetime

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
               RETURNING project_id;
    """
    
    curs.execute(query, (owner_id, title, description))
    
    project_id = curs.fetchone()[0]
    g.db_conn.commit()
    
    return project_id
    
def get_projects(user_id):
    curs = g.db_conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    query = """SELECT p.project_id, generate_join_code(p.project_id) as join_code, title, description
               FROM projects p
               LEFT JOIN project_members m ON m.project_id=p.project_id
               WHERE (p.owner_id = %(user_id)s
               OR m.user_id = %(user_id)s)
               AND not p.deleted;
    """
    
    curs.execute(query, {'user_id': user_id})
    r = curs.fetchall()
    
    return r