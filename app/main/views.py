from . import main_blue


@main_blue.route('/')
def index():
    return "It worked!"


@main_blue.route('/ping')
def ping():
    return "pong"
