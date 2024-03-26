from marshmallow import post_load

from Utilities.Config import ma, db


class FolderClassModel(db.Model):
    __tablename__ = 'folderClass'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    folder = db.Column(db.String(50))
    account = db.Column(db.String(45), db.ForeignKey('account.email'))
    classOn = db.Column(db.String(45), db.ForeignKey('classon.id'))

    def __init__(self, folder, account, classOn):
        self.folder = folder
        self.account = account
        self.classOn = classOn


class FolderClassSchema(ma.Schema):
    class Meta:
        fields = ('id', 'folder', 'account', 'classOn')

    @post_load
    def make_answer(self, data, **kwargs):
        return FolderClassModel(**data)


folderClassSchema = FolderClassSchema()
folderClassSchemas = FolderClassSchema(many=True)
