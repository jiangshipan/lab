from model.experiment import Experiment


class ExperimentDao(object):

    @staticmethod
    def get_all_experiments():
        return Experiment.query.all()

    @staticmethod
    def get_experiments_by_teacher_id(teacher_id):
        return Experiment.query.filter(Experiment.teacher_id == teacher_id).all()

    @staticmethod
    def get_experiments_by_status(status):
        return Experiment.query.filter(Experiment.status == status).all()

    @staticmethod
    def get_experiment_by_id(id):
        return Experiment.query.filter(Experiment.id == id).first()

    @staticmethod
    def get_experiments_by_teacher_id_pass(teacher_id):
        return Experiment.query.filter(Experiment.teacher_id == teacher_id, Experiment.status == Experiment.Status.SUCCESS).all()