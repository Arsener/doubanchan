from . import actor

@actor.route('/')
def index():
    return 'Hello, this is actor page'