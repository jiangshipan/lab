from wtforms import Form, StringField, validators
from flask import Blueprint, request

from service.experiment_service import ExperimentService
from utils.common_utils import validate_form
from utils.resp_utils import ResponseUtil

experiment = Blueprint('experiment', __name__)

experiment_service = ExperimentService()


@experiment.route("/add", methods=['POST'])
def add_experiment():
    """
    录入实验
    :return:
    """
    form = ExperimentAdd.from_json(formdata=request.json, meta={'locales': ['zh_CN', 'zh']})
    user_id = request.cookies.get('login_token').split('-')[0]
    try:
        validate_form(form)
        experiment_service.add_experiment(form.data, user_id)
    except Exception as e:
        return ResponseUtil.error_response(msg=str(e))
    return ResponseUtil.success_response(msg='success')

@experiment.route("/get")
def get_all_experiment():
    """
    得到实验
    :return:
    """
    user_id = request.cookies.get('login_token').split('-')[0]
    try:
        experiment_infos = experiment_service.get_all_experiments(user_id)
    except Exception as e:
        return ResponseUtil.error_response(data=[], msg=str(e))
    return ResponseUtil.success_response(data=experiment_infos, msg='success')

@experiment.route("/get_pass")
def get_all_experiment_pass():
    """
    得到实验
    :return:
    """
    user_id = request.cookies.get('login_token').split('-')[0]
    try:
        experiment_infos = experiment_service.get_all_experiments_pass(user_id)
    except Exception as e:
        return ResponseUtil.error_response(data=[], msg=str(e))
    return ResponseUtil.success_response(data=experiment_infos, msg='success')

@experiment.route("/join")
def join_experiment():
    """
    参加实验, 学生可选
    :return:
    """
    user_id = request.cookies.get('login_token').split('-')[0]
    try:
        eid = request.args.get('eid')
        experiment_service.join_experiment(user_id, int(eid))
    except Exception as e:
        return ResponseUtil.error_response(msg=str(e))
    return ResponseUtil.success_response(msg='success')

@experiment.route("/update")
def update_status():
    """
    修改实验状态  审批/拒绝
    :return:
    """
    user_id = request.cookies.get('login_token').split('-')[0]
    try:
        eid = request.args.get('eid')
        status = request.args.get('status')
        if not eid or not status:
            return ResponseUtil.error_response(msg="缺少相关参数")
        experiment_service.update_experiment(user_id, eid, int(status))
    except Exception as e:
        return ResponseUtil.error_response(msg=str(e))
    return ResponseUtil.success_response(msg='success')


class ExperimentAdd(Form):
    """
    录入实验Form
    """
    name = StringField(u'实验名称', [validators.Length(min=0, max=32), validators.required()])
    start_time = StringField(u'开始时间', [validators.required()])
    end_time = StringField(u'结束时间', [validators.required()])
    remark = StringField(u'实验备注', [validators.Length(min=0, max=512), validators.required()])
    lab_no = StringField(u"实验室名称", [validators.required()])
