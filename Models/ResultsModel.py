from marshmallow import post_load

from Models.AccountModel import AccountSchema
from Models.AnswerModel import AnswerSchema
from Models.QuestionModel import QuestionSchema
from Models.QuizzModel import QuizzSchema
from Utilities.Config import db, ma


class ResultsModel(db.Model):
    __tablename__ = "userresults"
    id = db.Column(db.Integer, primary_key=True)
    account = db.Column(db.String(45), db.ForeignKey('account.email'))
    quizz = db.Column(db.String(45), db.ForeignKey('quizz.id'))
    question = db.Column(db.Integer, db.ForeignKey('question.id'))
    answer = db.Column(db.Integer, db.ForeignKey('answer.id'))


class ResultsSchema(ma.Schema):
    class Meta:
        fields = ('id', 'account', 'quizz', 'question', 'answer')

    account_details = ma.Nested(AccountSchema, attribute='account_obj', dump_only=True)
    quizz_details = ma.Nested(QuizzSchema, attribute='quizz_obj', dump_only=True)
    question_details = ma.Nested(QuestionSchema, attribute='question_obj', dump_only=True)
    answer_details = ma.Nested(AnswerSchema, attribute='answer_obj', dump_only=True)

    @post_load
    def make_results(self, data, **kwargs):
        return ResultsModel(**data)


resultsSchema = ResultsSchema()
manyResultsSchema = ResultsSchema(many=True)
