from flask import Flask, request, redirect, render_template
import cgi

app = Flask(__name__)

app.config['DEBUG'] = True      # displays runtime errors in the browser, too


def is_blank(user_input):
    if user_input != '': #or user_input.isspace() or user_input.issymbol():
        return True
    else:
        return False

def match_password(password, v_password):
    if password == v_password:
        return True
    else:
        return False

def validate_user_and_pass(user_input):
    if len(user_input) < 3 or len(user_input) > 20:
        return False
    elif ' ' in user_input:
        return False
    else:
        return True

def validate_email(user_input):
    email = user_input
    if len(user_input) < 3 or len(user_input) > 20:
        return False
    elif ' ' in user_input:
        return False
    elif email.count('@') > 1 or email.count('.') > 1:
        return False
    else:
        return True

#The user provides an email, but it's not a valid email. Note: the email field may 
# be left empty, but if there is content in it, then it must be validated. 
# The criteria for a valid email address in this assignment are that it has 
# a single @, a single ., contains no spaces, and is between 3 and 20 characters long.


@app.route('/', methods=['POST'])
def validate_input():
    username = request.form['username']
    password = request.form['password']
    v_password = request.form['v_password']
    email = request.form['email']

    username_error = ''
    password_error = ''
    v_password_error = ''
    email_error = ''

    if not is_blank(password):
        password_error = 'Input field empty'
        v_password = ''
    elif not validate_user_and_pass(password):
        password_error = 'Not a valid password'
        v_password_error = password_error
        password = ''
        v_password = ''
    else:
        password =password
    if not match_password(password, v_password):
        v_password_error = 'Password does not match'
        v_password = ''
        password = ''
    elif not is_blank(v_password):
        v_password_error = 'Input field empty'
        password = ''
    else:
        v_password = v_password    
    if email == '':
        email = email
    else:
        if not validate_email(email):
            email_error = 'Not a valid email'
            password=''
            v_password=''
        else:
            email = email
    if not is_blank(username):
        username_error = 'Input field empty' 
        password = ''
        v_password = ''
    elif not validate_user_and_pass(username):
        username_error = 'Not a valid username'
        password = ''
        v_password = ''
    else:
        username = username
    if not username_error and not password_error and not v_password_error and not email_error:
        return render_template('welcome.html', username=username)
    else:
        return render_template('table_form.html', username_error=username_error,
        password_error=password_error, v_password_error=v_password_error,
        username=username, password=password, v_password=v_password,
        email_error=email_error)

@app.route('/') #, methods=['GET', 'POST'])
def index():
    return render_template('table_form.html', username_error='',
        password_error='', v_password_error='',
        username='', password='', v_password='')


app.run()