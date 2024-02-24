from Utilities.Config import db, ma
from marshmallow import fields, post_load


class CommentModel(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True)
    account = db.Column(db.String(45), db.ForeignKey('account.email'))
    post = db.Column(db.String(45), db.ForeignKey('post.id'))
    content = db.Column(db.String(45))
    dateComment = db.Column(db.DateTime)


class CommentSchema(ma.Schema):
    class Meta:
        fields = ('id', 'account', 'post', 'content', 'dateComment')

    @post_load
    def make_comment(self, data, **kwargs):
        return CommentModel(**data)


commentsSchema = CommentSchema(many=True)
commentSchema = CommentSchema()
