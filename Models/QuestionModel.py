from marshmallow import post_load

from Utilities.Config import db, ma


class QuestionModel(db.Model):
    __tablename__ = 'question'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    quizz = db.Column(db.String(50), db.ForeignKey('quizz.id'))


class QuestionSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'quizz')

    @post_load
    def make_question(self, data, **kwargs):
        return QuestionModel(**data)


questionsSchema = QuestionSchema(many=True)
questionSchema = QuestionSchema()
