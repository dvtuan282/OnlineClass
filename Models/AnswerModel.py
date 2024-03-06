from marshmallow import post_load

from Utilities.Config import db, ma


class AnswerModel(db.Model):
    __tablename__ = 'answer'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50))
    question = db.Column(db.String(45), db.ForeignKey('question.id'))
    isCorrect = db.Column(db.Integer)


class AnswerSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'question', 'isCrrect')

    @post_load
    def make_answer(self, data, **kwargs):
        return AnswerModel(**data)


answerSchema = AnswerSchema()
answersSchema = AnswerSchema(many=True)
