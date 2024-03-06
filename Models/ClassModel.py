from marshmallow import post_load

from Utilities.Config import db, ma
from Models.PostModel import PostModel
from Models.ClassMemberModel import ClassMemberModel
from Models.quizzClassModel import QuizzClassModel


class ClassModel(db.Model):
    __tablename__ = 'classon'
    id = db.Column(db.String(45), primary_key=True)
    className = db.Column(db.String(45))
    ''' creator chỉ là thuộc tính lưu gía trị khóa ngoại kiểu string, equale tên column trong db
        account.email là trỏ đến khóa chính của model account
    '''
    creator = db.Column(db.String(45), db.ForeignKey('account.email'))
    dateCreated = db.Column(db.Date)
    background = db.Column(db.String(45))
    post = db.relationship('PostModel', backref='class_post', lazy=True)
    classMember = db.relationship('ClassMemberModel', backref='class_classMember', lazy=True)
    quizzClass = db.relationship('QuizzClassModel', backref='class_quizzClass', lazy=True)


class ClassSchema(ma.Schema):
    class Meta:
        fields = ('id', 'className', 'creator', 'dateCreated', 'background')

    @post_load
    def make_classon(self, data, **kwargs):
        return ClassModel(**data)


classesSchema = ClassSchema(many=True)
classSchema = ClassSchema()
