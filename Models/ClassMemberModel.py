from Utilities.Config import db, ma
from marshmallow import fields, post_load


class ClassMemberModel(db.Model):
    __tablename__ = 'classMember'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    classOn = db.Column(db.String(45), db.ForeignKey('classon.id'))
    account = db.Column(db.String(45), db.ForeignKey('account.email'))
    status = db.Column(db.Integer, default=0)


class ClassMemberSchema(ma.SQLAlchemySchema):
    # classOn = ma.Nested(ClassSchema, only=('id', 'className', 'creator'))
    class Meta:
        model = ClassMemberModel
        fields = ('id', 'classOn', 'account', 'status')

    @post_load
    def make_classMember(self, data, **kwargs):
        return ClassMemberModel(**data)


classMemberSchema = ClassMemberSchema()
classesMemberSchema = ClassMemberSchema(many=True)
