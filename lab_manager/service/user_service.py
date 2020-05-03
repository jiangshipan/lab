import uuid
import json

from client.redis_client import redis_client
from dao.user_dao import UserDao
from model.user import User
from config.db import db


class UserService(object):
    """
    用户服务
    """

    def user_login(self, username, password):
        if not username or not password:
            raise Exception('username or password is empty')
        user = UserDao.get_user_by_username(username)
        if not user:
            raise Exception('user is not exist')
        if user.password != password:
            raise Exception('password is not available')
        token = self.assign_token(user.id)
        return token

    def user_register(self, user_info):
        """
        用户注册
        :param user_info:
        :return:
        """
        username = user_info.get('username')
        user = UserDao.get_user_by_username(username)
        if user:
            raise Exception('user has existed')
        try:
            user = User()
            user.username = username
            user.password = user_info.get('password')
            user.join_experiments = json.dumps([])
            db.session.add(user)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise Exception(e)

    def assign_token(self, user_id):
        """
        分配token. 1天过期
        :param username:
        :return:
        """
        token = redis_client.get(user_id)
        if not token:
            token = str(user_id) + '-' + ''.join(str(uuid.uuid4()).split('-'))
            redis_client.set(user_id, token, ex=1 * 3600 * 24)
        return token

    def get_user_info(self, user_id):
        user = UserDao.get_user_by_user_id(user_id)
        if not user:
            raise Exception("不存在该用户或被禁用")
        user_info = {
            'id': user.id,
            'username': user.username,
            'role': User.Role.__label__.get(user.role, '未知')
        }
        return user_info

    def get_user_infos(self):
        users = UserDao.get_all_users()
        res = []
        for user in users:
            res.append({
                'id': user.id,
                'username': user.username,
                'role': User.Role.__label__.get(user.role, '未知'),
                'contacts': user.contacts if user.contacts else "无"
            })
        return res

    def logout(self, user_id):
        redis_client.delete(user_id)

