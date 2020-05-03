from flask import Blueprint, request
from wtforms import Form, StringField, validators
from utils.common_utils import validate_form
from service.lab_service import LabService

from utils.resp_utils import ResponseUtil

laboratory = Blueprint('laboratory', __name__)

lab_service = LabService()


@laboratory.route("/getAll", methods=["GET"])
def get_laboratories():
    """
    获取实验室
    :return:
    """
    try:
        lab_infos = lab_service.get_all_labs()
    except Exception as e:
        return ResponseUtil.error_response(data=[], msg=str(e))
    return ResponseUtil.success_response(data=lab_infos, msg='success')

@laboratory.route("/add_help", methods=["GET"])
def help():
    """
    添加反馈
    :return:
    """
    try:
        lab_id = request.args.get('lab_id')
        question = request.args.get('question')
        lab_service.add_help(lab_id, question)
    except Exception as e:
        return ResponseUtil.error_response(msg=str(e))
    return ResponseUtil.success_response(msg='success')

@laboratory.route("/get_all_helps", methods=["GET"])
def get_help():
    """
    管理员查看反馈
    :return:
    """
    try:
        helps = lab_service.get_all_helps()
    except Exception as e:
        return ResponseUtil.error_response(data=[], msg=str(e))
    return ResponseUtil.success_response(data=helps, msg='success')

@laboratory.route("/do_help", methods=["GET"])
def do_help():
    """
    管理员处理反馈
    :return:
    """
    try:
        hid = request.args.get('hid')
        status = request.args.get('status')
        if not hid or not status:
            raise Exception("相关参数不能为空")
        lab_service.do_helps(hid, status)
    except Exception as e:
        return ResponseUtil.error_response(msg=str(e))
    return ResponseUtil.success_response(msg='success')

@laboratory.route("/add_new", methods=["POST"])
def add_new_lab():
    """
    新增实验室
    :return:
    """
    form = AddLabForm.from_json(formdata=request.json, meta={'locales': ['zh_CN', 'zh']})
    try:
        validate_form(form)
        lab_service.add_new_lab(form.data)
    except Exception as e:
        return ResponseUtil.error_response(msg=str(e))
    return ResponseUtil.success_response(msg='success')

@laboratory.route("/update", methods=["GET"])
def update_lab():
    """
    修改资产
    :return:
    """
    try:
        lab_id = request.args.get('lab_id')
        devices = request.args.get('devices')
        lab_service.update_lab_device(lab_id, devices)
    except Exception as e:
        return ResponseUtil.error_response(msg=str(e))
    return ResponseUtil.success_response(msg='success')

class AddLabForm(Form):
    """
    自定义注册Form
    """
    name = StringField(u'实验室名称', [validators.Length(min=0, max=32), validators.required()])
    notice = StringField(u'公告/规章', [validators.Length(min=0, max=512), validators.required()])
    devices = StringField(u'公告/规章', [validators.Length(min=0, max=512), validators.required()])
