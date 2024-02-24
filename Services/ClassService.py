from datetime import datetime

from flask import Flask, request, jsonify
from sqlalchemy import and_
from sqlalchemy.sql.functions import current_user

from Models.ClassMemberModel import ClassMemberModel
from Utilities.RamdomCode import ramdomCode
from Models.ClassModel import classSchema, classesSchema, ClassModel
from flask_login import current_user
from Models.AccountModel import AccountModel
from Utilities.Config import db


def listClassOfAccount():
    account = AccountModel.query.get(current_user.email)
    classOn = [cl for cl in account.classOn]
    return jsonify(classesSchema.dump(classOn))


def listOfClassInvolved():
    listClass = db.session.query(ClassModel).join(ClassMemberModel, ClassMemberModel.classOn == ClassModel.id). \
        join(AccountModel, AccountModel.email == ClassMemberModel.account). \
        filter(and_(AccountModel.email == current_user.email, ClassMemberModel.status == 1)).all()
    return listClass


def createClass():
    data = request.json
    data['id'] = ramdomCode()
    data['dateCreated'] = datetime.now().date()
    data['creator'] = current_user.email
    data['background'] = 'backgrouClassDefault.jpg'
    try:
        classOn = classSchema.load(data)
        db.session.add(classOn)
        db.session.commit()
        return jsonify({'message': 'create class successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'{str(e)}'})


def informationClass(idClass):
    classOn = ClassModel.query.get(idClass)
    return jsonify(classSchema.dump(classOn))


def updateClass(idClass):
    pass


def deleteClass(idClass):
    pass
