
from flask import Blueprint, request

from service.email_service import EmailService
from utils.resp_utils import ResponseUtil

email = Blueprint('email', __name__)

email_service = EmailService()


@email.route("/add", methods=["GET"])
def send_msg():
    """
    发送消息/公告
    :return:
    """
    user_id = request.cookies.get('login_token').split('-')[0]
    try:
        eid = request.args.get('eid')
        content = request.args.get('content')
        if not content:
            raise Exception('相关参数不能为空')
        email_service.send_msg_v1(user_id, eid, content)
    except Exception as e:
        return ResponseUtil.error_response(msg=str(e))
    return ResponseUtil.success_response(msg='发送成功')

@email.route("/get")
def get_msg():
    """
    显示站内信
    :return:
    """
    user_id = request.cookies.get('login_token').split('-')[0]
    try:
        res = email_service.get_all_msgs(user_id)
    except Exception as e:
        return ResponseUtil.error_response(data=[], msg=str(e))
    return ResponseUtil.success_response(data=res, msg='success')