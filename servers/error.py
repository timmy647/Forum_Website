from flask import Flask, request, jsonify
from werkzeug.exceptions import HTTPException
from flask_cors import CORS
from json import dumps

def defaultHandler(err):
    response = err.get_response()
    response.data = dumps({
        "code": err.code,
        "name": "System Error",
        "message": err.description,
    })
    response.content_type = 'application/json'
    return response

APP = Flask(__name__)
APP.config['TRAP_HTTP_EXCEPTIONS'] = True
APP.register_error_handler(Exception, defaultHandler)
CORS(APP)

class ValueError(HTTPException):
    message = 'No message specified'

class AccessError(HTTPException):
    message = 'No message specified'

# Post
@APP.route('/invalidemail')
def invalid_email():
    raise ValueError("Invalid email")
    pass

@APP.route('/unregisteremail')
def unregister_email():
    raise ValueError("Unregistered email")
    pass

@APP.route('/registeredemail')
def registered_email():
    raise ValueError("Registered email")
    pass

@APP.route('/incorrectpassword')
def incorrect_password():
    raise ValueError("Incorrect password")
    pass

@APP.route('/invalidtoken')
def invalid_token():
    raise ValueError("Invalid Token")
    pass

@APP.route('/inputtoolong')
def input_too_long():
    raise ValueError("Input is too long")
    pass

@APP.route('/inputtooshort')
def input_too_short():
    raise ValueError("Input is too short")
    pass

@APP.route('/invalidcode')
def invalid_code():
    raise ValueError("Invalid code")
    pass



if __name__ == '__main__':
    APP.run(debug=True)



