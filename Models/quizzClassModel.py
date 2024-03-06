from marshmallow import post_load

from Utilities.Config import db, ma


class QuizzClassModel(db.Model):
    __tablename__ = 'quizzClass'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    quizz = db.Column(db.String(45), db.ForeignKey('quizz.id'))
    classOn = db.Column(db.String(45), db.ForeignKey('classon.id'))


class QuizzClassSchema(ma.Schema):
    class Meta:
        fields = ('id', 'quizz', 'classOn')

    @post_load
    def make_quizzClass(self, data, **kwargs):
        return QuizzClassModel(**data)


quizzesClass = QuizzClassSchema(many=True)
quizzClass = QuizzClassSchema()
