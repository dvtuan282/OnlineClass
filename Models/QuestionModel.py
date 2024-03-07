from marshmallow import post_load

from Utilities.Config import db, ma
from Models.AnswerModel import AnswerSchema, AnswerModel


class QuestionModel(db.Model):
    __tablename__ = 'question'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    quizz = db.Column(db.String(50), db.ForeignKey('quizz.id'))
    answer = db.relationship('AnswerModel', backref='question_answer', lazy=True)


class QuestionSchema(ma.Schema):
    answer = ma.Nested(AnswerSchema, many=True)

    class Meta:
        fields = ('id', 'title', 'answer')

    @post_load
    def make_question(self, data, **kwargs):
        return QuestionModel(**data)


questionsSchema = QuestionSchema(many=True)
questionSchema = QuestionSchema()
