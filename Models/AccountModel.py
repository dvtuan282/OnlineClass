from marshmallow import post_load
from Utilities.Config import ma, db, login_manager
from flask_login import UserMixin
from Models.ClassModel import ClassModel
from Models.PostModel import PostModel
from Models.CommentModel import CommentModel
from Models.ClassMemberModel import ClassMemberModel


class AccountModel(UserMixin, db.Model):
    __tablename__ = 'account'
    email = db.Column(db.String(50), primary_key=True)
    password = db.Column(db.String(45))
    name = db.Column(db.String(45))
    avatar = db.Column(db.String(45))
    """ 
        -Khi đặt relationship tại 1 trong 2 bảng có mỗi quan hệ với nhau, thì chúng
        ta có thể truy cập thuộc tính của đối tượng này thông qua đối tượng kia
        - ClassOnModel: tên của lớp
        - từ lớp kia khi truy cập đến các thuộc tính của lớp này sử dụng _backref='account_comment'_
        """
    classOn = db.relationship('ClassModel', backref='account_class', lazy=True)
    post = db.relationship('PostModel', backref='account_post', lazy=True)
    comment = db.relationship('CommentModel', backref='account_comment', lazy=True)
    classMember = db.relationship('ClassMemberModel', backref='account_classMember', lazy=True)

    '''Phương thức get_id được ghi đè lại từ UserMixin, do get_id nhận vào giá trị là id nhưng
    lớp account không có trường id nên phải định nghĩa lại.'''

    def get_id(self):
        return str(self.email)

    @login_manager.user_loader
    def load_account(email):
        return AccountModel.query.get(email)


class AccountSchema(ma.Schema):
    class Meta:
        fields = ('email', 'password', 'name', 'avatar')

    @post_load
    def make_account(self, data, **kwargs):
        return AccountModel(**data)


accountsSchema = AccountSchema(many=True)
accountSchema = AccountSchema()
