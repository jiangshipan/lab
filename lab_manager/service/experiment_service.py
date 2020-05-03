import json
from dao.experiment_dao import ExperimentDao
from dao.laboratory_dao import LaboratoryDao
from dao.user_dao import UserDao
from model.experiment import Experiment
from model.user import User
from service.email_service import EmailService
from utils.common_utils import time2datetime
from config.db import db

email_service = EmailService()

class ExperimentService(object):
    """
    实验管理
    """

    def add_experiment(self, info, user_id):
        try:
            experiment = Experiment()
            experiment.name = info.get('name')
            experiment.start_time = time2datetime(info.get('start_time'))
            experiment.end_time = time2datetime(info.get('end_time'))
            if experiment.start_time > experiment.end_time:
                raise Exception(u"开始时间不能大于结束时间")
            experiment.remark = info.get('remark')
            experiment.lab_no = info.get('lab_no')
            experiment.teacher_id = user_id
            experiment.status = Experiment.Status.PROCESS
            db.session.add(experiment)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise Exception(e)

    def get_all_experiments(self, user_id):
        """
        根据user_id的身份获取所有实验
        :param user_id:
        :return:
        """
        user = UserDao.get_user_by_user_id(user_id)
        experiments = []
        if user.role == User.Role.MANAGER:
            # 管理员可见所有
            experiments = ExperimentDao.get_all_experiments()
        elif user.role == User.Role.TEACHER:
            # 老师仅可见自己的
            experiments = ExperimentDao.get_experiments_by_teacher_id(user_id)
        elif user.role == User.Role.STUDENT:
            # 学生仅可见审批通过的
            experiments = ExperimentDao.get_experiments_by_status(Experiment.Status.SUCCESS)
        lab_ids = [_.lab_no for _ in experiments]
        laboratories = LaboratoryDao.get_lab_by_ids(lab_ids)
        lab_no2name = {_.id: _.name for _ in laboratories}
        res = []
        for experiment in experiments:
            # 查询所有选择该实验的学生
            students = UserDao.get_all_student()
            all_select_names = []
            for student in students:
                join_list = json.loads(student.join_experiments)
                if experiment.id in join_list:
                    all_select_names.append(student.username)
            teacher_name = UserDao.get_user_by_user_id(experiment.teacher_id).username
            res.append({
                'id': experiment.id,
                'name': experiment.name,
                'start_time': experiment.start_time.strftime('%Y-%m-%d %H:%M:%S'),
                'end_time': experiment.end_time.strftime('%Y-%m-%d %H:%M:%S'),
                'remark': experiment.remark,
                'lab_name': lab_no2name.get(experiment.lab_no, '未知'),
                'teacher_name': teacher_name,
                'status': Experiment.Status.__label__.get(experiment.status, '未知'),
                'all_selects': all_select_names
            })
        return res

    def get_all_experiments_pass(self, user_id):
        """
        根据user_id的身份获取所有实验
        :param user_id:
        :return:
        """
        user = UserDao.get_user_by_user_id(user_id)

        if user.role != User.Role.TEACHER:
            raise Exception("仅有老师有权限")

        experiments = ExperimentDao.get_experiments_by_teacher_id_pass(user_id)

        lab_ids = [_.lab_no for _ in experiments]
        laboratories = LaboratoryDao.get_lab_by_ids(lab_ids)
        lab_no2name = {_.id: _.name for _ in laboratories}
        res = []
        for experiment in experiments:
            # 查询所有选择该实验的学生
            students = UserDao.get_all_student()
            all_select_names = []
            for student in students:
                join_list = json.loads(student.join_experiments)
                if experiment.id in join_list:
                    all_select_names.append(student.username)
            teacher_name = UserDao.get_user_by_user_id(experiment.teacher_id).username
            res.append({
                'id': experiment.id,
                'name': experiment.name,
                'start_time': experiment.start_time.strftime('%Y-%m-%d %H:%M:%S'),
                'end_time': experiment.end_time.strftime('%Y-%m-%d %H:%M:%S'),
                'remark': experiment.remark,
                'lab_name': lab_no2name.get(experiment.lab_no, '未知'),
                'teacher_name': teacher_name,
                'status': Experiment.Status.__label__.get(experiment.status, '未知'),
                'all_selects': all_select_names
            })
        return res

    def join_experiment(self, user_id, eid):
        """
        参加某个实验
        :return:
        """
        user = UserDao.get_user_by_user_id(user_id)
        if user.role != User.Role.STUDENT:
            raise Exception("只有学生可选")
        try:
            experiments = json.loads(user.join_experiments)
            experiments.append(eid)
            user.join_experiments = json.dumps(experiments)
            experiment = ExperimentDao.get_experiment_by_id(eid)
            user = UserDao.get_user_by_user_id(experiment.teacher_id)
            email = email_service.send_msg(experiment.teacher_id, user.username, user_id, u'欢迎参加%s实验' % experiment.name)
            db.session.add(email)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise Exception(str(e))

    def update_experiment(self, user_id, eid, status):
        """
        修改实验状态
        :param status:
        :param user_id:
        :param eid:
        :return:
        """
        user = UserDao.get_user_by_user_id(user_id)
        if user.role != User.Role.MANAGER:
            raise Exception("只有管理员可以审批")
        experiment = ExperimentDao.get_experiment_by_id(eid)
        if not experiment:
            raise Exception("不存在该计划")
        try:
            experiment.status = status
            content = ''
            if status == Experiment.Status.SUCCESS:
                content = '您的实验:%s, 已经审批通过。' % experiment.name
            elif status == Experiment.Status.FAILED:
                content = '您的实验:%s, 审批未通过, 请联系系统管理员重新申请。' % experiment.name
            email = email_service.send_msg(user_id, u'系统管理员', experiment.teacher_id, content)
            db.session.add(email)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise Exception(str(e))






