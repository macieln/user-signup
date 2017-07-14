from flask import Flask, request, redirect, render_template
import cgi

app = Flask(__name__)

app.config['DEBUG'] = True

def lenght_validate(text, min_lenght):
    return len(list(text)) > min_lenght

def space_check(text):
    for character in list(text):
        if character == ' ':
            return True

    return False

def validate_email(text):
    period = False
    at = True
    for character in list(text):
        if character == '.':
            period = True
        if character == '@':
            at = True

    if period and at:
        return True
    else:
        return False

@app.route('/')
def signup():
    username = request.args.get('username')
    email = request.args.get('email')
    username_error = request.args.get('username_error')
    password_error = request.args.get('password_error')
    verify_error = request.args.get('verify_error')
    email_error = request.args.get('email_error')

    if username == None:
        username = ''
    if username_error == None:
        username_error = ''
    if password_error == None:
        password_error = ''
    if verify_error == None:
        verify_error = ''
    if email == None:
        email = ''
    if email_error == None:
        email_error = ''

    print(username)
    print(email)

    return render_template("signup-form.html", username=username, email=email, username_error=username_error, password_error=password_error, verify_error=verify_error, email_error=email_error)

@app.route('/signup', methods=['post'])
def validate():
    username = request.form['username']
    password = request.form['password']
    password_verify = request.form['verify-password']
    email = request.form['email']

    username_error = ''
    password_error = ''
    verify_error = ''
    email_error = ''

    if username == '':
        username_error = 'Invalid Username'
    elif not lenght_validate(username, 3) or lenght_validate(username, 20):
        username_error = 'Invalid Username Lenght'
    elif space_check(username):
        username_error = 'Space Is Not An Acceptable Character'

    if password == '':
        password_error = 'Invalid Password'
    elif not lenght_validate(password, 3) or lenght_validate(password, 20):
        password_error = 'Invalid Password Lenght'
    elif space_check(password):
        password_error = 'Space Is Not An Acceptable Character'
    elif password_verify != password:
        verify_error = 'Passwords Do Not Match'

    if email:
        if not validate_email(email):
            email_error = 'Invalid Email'

    if username_error or password_error or verify_error or email_error:
        return redirect('/?username=' + username + '&email=' + email + '&username_error=' + username_error + '&password_error=' + password_error + '&verify_error=' + verify_error + '&email_error=' + email_error)
    else:
        return redirect('/welcome?username=' + username)

@app.route('/welcome')
def welcome_message():
    username = request.args.get('username')

    return render_template('confirmation-form.html', username=username)
app.run()
