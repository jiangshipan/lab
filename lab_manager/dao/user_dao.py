from model.user import User


class UserDao(object):

    @staticmethod
    def get_user_by_username(username):
        return User.query.filter(User.username == username).first()


    @staticmethod
    def get_user_by_user_id(user_id):
        return User.query.filter(User.id == user_id).first()

    @staticmethod
    def get_all_users():
        return User.query.filter(User.role != User.Role.MANAGER).all()

    @staticmethod
    def get_all_student():
        return User.query.filter(User.role == User.Role.STUDENT).all()