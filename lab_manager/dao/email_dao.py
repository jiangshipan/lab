from model.email import Email


class EmailDao(object):

    @staticmethod
    def get_emails_by_user_id(user_id):
        return Email.query.filter(Email.user_id == user_id).order_by(Email.create_time.desc()).all()