from flask import Blueprint

# Create a blueprint for the 'test' module
test = Blueprint('test', __name__)

# Define a route for the 'test' module
@test.route('/')
def hello_world():
    return "Hello, World!"
