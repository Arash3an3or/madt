import quart.flask_patch

import sys
import os

from net_control import net_control_bp
from lab_visualization import lab_visual_bp
from lab_control import lab_control_bp
from cluster_control import cluster_control_bp
from login import login_bp, login_manager

from config import labs_dir

# from flask import Flask, render_template, session, request
from quart import Quart, render_template, session, request
from flask_login import login_required

# app = Flask(__name__)
app = Quart(__name__)
app.register_blueprint(net_control_bp)
app.register_blueprint(lab_visual_bp)
app.register_blueprint(lab_control_bp)
app.register_blueprint(cluster_control_bp)
app.register_blueprint(login_bp)

login_manager.init_app(app)
app.secret_key = b'lksv5533_-=23scvvd\n\n'

@app.route('/')
async def list_labs():

    labs = os.listdir(labs_dir)

    print('labs', labs)

    return await render_template('labs_list.html', labs=labs)


@app.before_request
def check_valid_login():
    login_valid = 'user_id' in session and session.get('user_id') is not None

    if (request.endpoint and
        'static' not in request.endpoint and
        not login_valid and
        not getattr(app.view_functions[request.endpoint], 'is_public', False)):
        return render_template('login.html', next=request.endpoint)



if __name__ == '__main__':

    if len(sys.argv) != 2 and len(sys.argv) != 3:
        print('Usage: sudo python main.py [port] [-t]')
        sys.exit(0)

    '''
    if os.getuid() != 0:
        print('Wrong UID: {0}\nUsage: sudo python main.py [port]'.format(os.getuid()))
        sys.exit(0)
    '''

    if len(sys.argv) == 3 and sys.argv[2] == '-t':
        print('Running server in threaded mode...')
        app.run(host='0.0.0.0', port=sys.argv[1], debug=True)
    elif len(sys.argv) == 3 and sys.argv[2] == '-p':
        print('Running server in profiling mode...')
        from werkzeug.middleware.profiler import ProfilerMiddleware

        app.config['PROFILE'] = True
        app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=[30])
        app.run(host='0.0.0.0', port=sys.argv[1], debug=True)

    elif len(sys.argv) == 3 and sys.argv[2] == '-q':
        print('Running server in quart mode...')
        app.run(host='0.0.0.0', port=sys.argv[1], debug=False, threaded=False, processes=1)

    else:
        print('Running server in un-threaded mode...')
        app.run(host='0.0.0.0', port=sys.argv[1], debug=True, threaded=False, processes=1)








