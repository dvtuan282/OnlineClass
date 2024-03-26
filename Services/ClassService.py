import json
from datetime import datetime
from google.oauth2.credentials import Credentials
from flask import Flask, request, jsonify, session
from sqlalchemy import and_
from sqlalchemy.sql.functions import current_user
import Services.DaoService as daoService
from Models.ClassMemberModel import ClassMemberModel
from Utilities.RamdomCode import ramdomCode
from Models.ClassModel import classSchema, classesSchema, ClassModel
from flask_login import current_user
from Models.AccountModel import AccountModel
from Utilities.Config import db
import Services.LoginGoogleService as loginGoogle


def listClassOfAccount():
    account = AccountModel.query.get(current_user.email)
    classOn = [cl for cl in account.classOn]
    return jsonify(classesSchema.dump(classOn))


def listClassOfAccountObject():
    account = AccountModel.query.get(current_user.email)
    classOn = [cl for cl in account.classOn]
    return classOn


def listOfClassInvolved():
    listClass = db.session.query(ClassModel).join(ClassMemberModel, ClassMemberModel.classOn == ClassModel.id). \
        join(AccountModel, AccountModel.email == ClassMemberModel.account). \
        filter(and_(AccountModel.email == current_user.email, ClassMemberModel.status == 0)).all()
    return classesSchema.dump(listClass)


def createClass():
    data = request.json
    data['id'] = ramdomCode()
    data['dateCreated'] = datetime.now().date()
    data['creator'] = current_user.email
    data['background'] = 'backgrouClassDefault.jpg'
    creds = Credentials.from_authorized_user_info(json.loads(session['creds']))
    idFolder = loginGoogle.createFolder(creds, data['className'], current_user.idFolder)
    data['folder'] = idFolder
    classOn = classSchema.load(data)
    daoService.create(classOn)
    return jsonify({"message": "Create class successfully"})


def informationClass(idClass):
    classOn = ClassModel.query.get(idClass)
    return jsonify(classSchema.dump(classOn))


def updateClass(idClass):
    pass


def deleteClass(idClass):
    pass
