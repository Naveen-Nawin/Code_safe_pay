from flask import Flask, render_template, request
import pyotp

app = Flask(__name__)

# Secret key for session management (change this to a secure random key in production)
app.secret_key = 'your_secret_key'

# Dummy user data (replace this with actual user authentication logic)
users = {
    'user1': {
        'password': 'password123',
        'authenticator_secret': 'JBSWY3DPEHPK3PXP'
    }
}

# Dummy database to store generated OTPs
otp_database = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_otp', methods=['POST'])
def generate_otp():
    username = request.form['username']
    password = request.form['password']

    if username in users and users[username]['password'] == password:
        if username not in otp_database:
            otp_database[username] = pyotp.TOTP(users[username]['authenticator_secret'])

        otp = otp_database[username].now()
        return {'otp': otp}
    else:
        return {'error': 'Invalid username or password'}, 401

@app.route('/validate_authenticator', methods=['POST'])
def validate_authenticator():
    username = request.form['username']
    authenticator_code = request.form['authenticator_code']

    if username in users and pyotp.TOTP(users[username]['authenticator_secret']).verify(authenticator_code):
        return {'valid': True}
    else:
        return {'valid': False}, 401

if __name__ == '__main__':
    app.run(debug=True)
