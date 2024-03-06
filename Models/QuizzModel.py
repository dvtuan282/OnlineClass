from marshmallow import post_load

from Utilities.Config import db, ma
from Models.quizzClassModel import QuizzClassModel


class QuizzModel(db.Model):
    __tablename__ = 'quizz'
    id = db.Column(db.String(45), primary_key=True)
    title = db.Column(db.String(100))
    openTime = db.Column(db.DateTime)
    closedTime = db.Column(db.DateTime)
    testTime = db.Column(db.Integer)
    image = db.Column(db.String(50))
    status = db.Column(db.Integer)
    quizzClass = db.relationship('QuizzClassModel', backref='quizz_quizzClass', lazy=True)


class QuizzSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'openTime', 'closedTime', 'testTime', 'image', 'status')

    @post_load
    def make_quizz(self, data, **kwargs):
        return QuizzModel(**data)


quizzSchema = QuizzSchema()
quizzesSchema = QuizzSchema(many=True)
