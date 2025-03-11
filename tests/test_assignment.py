import pytest
import os
import sqlite3

@pytest.fixture(scope="session")
def setup_database():
    os.popen('sqlite3 _temp.db < reset.sql').read()
    os.popen('sqlite3 _temp.db < 1.sql').read()
    os.popen('sqlite3 _temp.db < 2.sql').read()
    yield
    os.popen('rm _temp.db').read()

def test_q1_use_update():
    assert 'update' in open('1.sql').read().lower(), "You need to use UPDATE statement in 1.sql"
    
def test_q1_reset_password(setup_database):
    conn = sqlite3.connect('_temp.db')
    admin_password = conn.execute("select password from users where username = 'admin'").fetchall()
    assert 'bd133ca9896' in admin_password[0][0] 

def test_q1_login():
    import subprocess

    try:
        process = subprocess.Popen(['python','app.py','opps!'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate(timeout=1)  # Timeout after 5 seconds
    except subprocess.TimeoutExpired:
        process.kill()
        stdout, stderr = process.communicate()  # Ensure process cleanup
        
    assert b'POS' in stdout, "Not able to login with opps! as password" 
    
def test_q2_use_emily33():
    assert 'emily33' in open('2.sql').read().lower(), "You need to use emily33 in 2.sql"

def test_q2_fake_log(setup_database):
    conn = sqlite3.connect('_temp.db')
    password = conn.execute("select new_password from user_logs where old_username = 'admin' and new_username = 'admin' and type='update'").fetchall()
    assert password[0][0] == '44bf025d27eea66336e5c1133c3827f7'
