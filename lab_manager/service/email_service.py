from dao.email_dao import EmailDao
from dao.user_dao import UserDao
from model.email import Email
from config.db import db
from model.user import User
import json


class EmailService(object):
    """
    邮箱服务
    """

    def send_msg(self, create_id, create_name, target_id, content):
        """
        发送消息通用方法
        :param create_name:
        :param create_id:
        :param target_id:
        :param content:
        :return:
        """
        email = Email()
        email.user_id = target_id
        email.create_id = create_id
        email.create_name = create_name
        email.content = content
        return email

    def get_all_msgs(self, user_id):
        """
        获取某人所有邮件
        :param user_id:
        :return:
        """
        emails = EmailDao.get_emails_by_user_id(user_id)
        res = []
        for email in emails:
            res.append({
                'content': email.content,
                'create_name': email.create_name,
                'create_time': email.create_time.strftime('%Y-%m-%d %H:%M:%S'),
            })
        return res

    def send_msg_v1(self, user_id, eid, content):
        """
        发送消息
        :param user_id:
        :param eid:
        :param content:
        :return:
        """
        try:
            user = UserDao.get_user_by_user_id(user_id)
            add_emails = []
            if user.role == User.Role.MANAGER:
                # 发消息人是管理员, 给所有人发送
                users = UserDao.get_all_users()
                for user_ in users:
                    email = self.send_msg(user_id, '系统管理员', user_.id, content)
                    add_emails.append(email)
            elif user.role == User.Role.STUDENT:
                # 发消息人是老师, 给当前选实验的人发送
                students = UserDao.get_all_student()
                for student in students:
                    join_list = json.loads(student.join_experiments)
                    if eid in join_list:
                        # 当前用户选修了该实验
                        email = self.send_msg(user_id, user.username, student.id, content)
                        add_emails.append(email)
            db.session.bulk_save_objects(add_emails)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise Exception(str(e))




