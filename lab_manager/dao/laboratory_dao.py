from model.help import Help
from model.laboratory import Laboratory


class LaboratoryDao(object):

    @staticmethod
    def get_all_labs():
        return Laboratory.query.all()


    @staticmethod
    def get_lab_by_ids(ids):
        return Laboratory.query.filter(Laboratory.id.in_(ids)).all()


    @staticmethod
    def get_all_helps():
        return Help.query.all()

    @staticmethod
    def get_help_by_id(id):
        return Help.query.filter(Help.id == id).first()