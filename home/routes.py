from home import home

@home.route('/')
@home.route('/index')
def index():
    return "Hello, World!"