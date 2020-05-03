from config.db import app
from flask import request
from api.user import user
from api.experiment import experiment
from api.laboratory import laboratory
from api.email import email
from client.redis_client import redis_client
from utils.resp_utils import ResponseUtil

app.register_blueprint(user, url_prefix='/user')
app.register_blueprint(experiment, url_prefix='/experiment')
app.register_blueprint(laboratory, url_prefix='/laboratory')
app.register_blueprint(email, url_prefix='/email')

@app.route('/')
def hello_world():
    return 'Hello World!'

# 不进行校验的方法
ALLOW_METHOD = ['/user/login', '/user/reg']


@app.before_request
def check_token():
    """
    校验身份
    :return:
    """
    method = str(request.url_rule)
    if not method or method not in ALLOW_METHOD:
        login_token = request.cookies.get('login_token')
        if not login_token:
            return ResponseUtil.error_response(msg='no access')
        user_id = login_token.split('-')[0]
        real_token = redis_client.get(user_id)
        if real_token:
            # 因为python3 从redis返回的是b'', 即ascll码, py3是unicode
            real_token = real_token.decode()
        if login_token != real_token:
            return ResponseUtil.error_response(msg='no access')
    return

@app.after_request
def cors(environ):
    """
    解决跨域
    :param environ:
    :return:
    """
    environ.headers['Access-Control-Allow-Origin'] = request.headers.get('Origin')
    environ.headers['Access-Control-Allow-Method'] = '*'
    environ.headers['Access-Control-Allow-Headers'] = 'x-requested-with, content-type'
    environ.headers['Access-Control-Allow-Credentials'] = 'true'
    return environ

if __name__ == '__main__':
    app.run(debug=True)
