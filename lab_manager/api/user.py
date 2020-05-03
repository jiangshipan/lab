from wtforms import Form, StringField, validators
from flask import Blueprint, request, make_response

from service.user_service import UserService
from utils.common_utils import validate_form
from utils.resp_utils import ResponseUtil

user = Blueprint('user', __name__)

user_service = UserService()


@user.route("/login", methods=["GET"])
def login():
    """
    登陆接口
    :return:
    """
    username = request.args.get('username')
    password = request.args.get('password')
    try:
        msg = user_service.user_login(username, password)
        resp = make_response('{"msg": "success", "code": 0, "data": null}')
        resp.set_cookie("login_token", msg, max_age=1 * 3600 * 24)
    except Exception as e:
        return ResponseUtil.error_response(msg=str(e))
    return resp

@user.route("/reg", methods=['POST'])
def register():
    """
    注册接口
    :return:
    """
    form = RegisterForm.from_json(formdata=request.json, meta={'locales': ['zh_CN', 'zh']})
    try:
        validate_form(form)
        user_service.user_register(form.data)
    except Exception as e:
        return ResponseUtil.error_response(msg=str(e))
    return ResponseUtil.success_response(msg='success')

@user.route("/get")
def get_user_info():
    """
    获取当前登陆用户的信息
    :return:
    """
    user_id = request.cookies.get('login_token').split('-')[0]
    try:
        user_info = user_service.get_user_info(user_id)
    except Exception as e:
        return ResponseUtil.error_response(data={}, msg=str(e))
    return ResponseUtil.success_response(data=user_info, msg='success')

@user.route("/getAll")
def get_all_user():
    """
    查询所有用户
    :return:
    """
    try:
        user_infos = user_service.get_user_infos()
    except Exception as e:
        return ResponseUtil.error_response(data=[], msg=str(e))
    return ResponseUtil.success_response(data=user_infos, msg='success')

@user.route("/logout")
def logout():
    """
    用户注销
    :return:
    """
    user_id = request.cookies.get('login_token').split('-')[0]
    try:
        user_service.logout(user_id)
    except Exception as e:
        return ResponseUtil.error_response(msg=str(e))
    return ResponseUtil.success_response(msg='success')

class RegisterForm(Form):
    """
    自定义注册Form
    """
    username = StringField(u'用户名', [validators.Length(min=4, max=32), validators.required()])
    password = StringField(u'密码', [validators.Length(min=4, max=32), validators.required()])
