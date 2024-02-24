from Utilities.Config import db, ma
from marshmallow import fields, post_load
from Models.CommentModel import CommentModel, CommentSchema


class PostModel(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True)
    account = db.Column(db.String(45), db.ForeignKey('account.email'))
    classOn = db.Column(db.String(45), db.ForeignKey('classon.id'))
    datePosted = db.Column(db.DateTime)
    content = db.Column(db.String(45))
    comment = db.relationship('CommentModel', backref='post_comment', lazy=True)


class PostSchema(ma.SQLAlchemySchema):
    # ma.nested để bao gồm schema con trong một schema cha
    comment = ma.Nested(CommentSchema, many=True)

    class Meta:
        fields = ('id', 'account', 'classOn', 'datePosted', 'content', 'comment')

    @post_load
    def make_post(self, data, **kwargs):
        return PostModel(**data)


postsSchema = PostSchema(many=True)
postSchema = PostSchema()
