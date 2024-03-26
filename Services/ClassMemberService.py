import json

import unicodedata
from flask import request, jsonify, session
from flask_login import current_user
import pandas as pd
from google.oauth2.credentials import Credentials
from Models.FolderClassModel import FolderClassModel, folderClassSchema
from Models.ClassMemberModel import classesMemberSchema, classMemberSchema, ClassMemberModel
from Models.ClassModel import ClassModel
from Utilities.Config import db
from Models.AccountModel import AccountModel
from Utilities.Email import sendEmailTemplate
import Services.LoginGoogleService as loginGoogle
import Services.DaoService as daoService


def createMemberInClass():
    data = request.json
    classOn = data['classOn']
    classOnModel = ClassModel.query.get(classOn)
    adminClass = AccountModel.query.get(current_user.email)

    try:
        for email in data['accounts']:
            classMember = ClassMemberModel()
            classMember.classOn = classOn
            classMember.account = email
            classMember.status = 1
            db.session.add(classMember)
            db.session.commit()
            sendEmailTemplate(email, 'MỜI THAM GIA LỚP HỌC', '/default/mail/moiThamGia.html', accountClass=adminClass,
                              classOn=classOnModel, email=email)
        return jsonify({'message': 'Oke'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': str(e)})


def confirmJoinClass(idCLassMember):
    try:
        classMember = ClassMemberModel.query.get(idCLassMember)
        classMember.status = 0
        db.session.commit()
        creds = Credentials.from_authorized_user_info(json.loads(session['creds']))
        idFolder = loginGoogle.createFolder(creds, classMember.class_classMember.className, current_user.idFolder)
        folderClass = FolderClassModel(idFolder, current_user.email, classMember.classOn)
        print(folderClass.classOn)
        daoService.create(folderClass)
        return jsonify({'message': 'Join class seccessfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'{str(e)}'}), 500


def deleteMember(idClassMember):
    try:
        classMember = ClassMemberModel.query.get(idClassMember)
        db.session.delete(classMember)
        db.session.commit()
        return jsonify({'message': 'Delete member successfully'})
    except Exception as e:
        db.session.commit()
        return jsonify({'message': f'{str(e)}'})


def showMemberInClass(idClass):
    members = ClassMemberModel.query.filter_by(classOn=idClass)
    return jsonify(classesMemberSchema.dump(members))


def createMembersInClass(classOn):
    try:
        # kiểm tra file có được gửi lên không
        if 'file' not in request.files:
            return jsonify({'message': 'No file part'}), 400
        file = request.files['file']
        if file.filename == '' and file.filename.endswith('.xlsx'):
            return jsonify({"message": "No selected file"}), 400
        df = pd.read_excel(file)
        # Chuẩn hóa dataframe bị lỗi utf8
        df['Email'] = df['Email'].apply(
            lambda x: unicodedata.normalize('NFD', str(x)).encode('ascii', 'ignore').decode('utf-8'))

        classOnModel = ClassModel.query.get(classOn)
        adminClass = AccountModel.query.get(current_user.email)
        for email in df['Email']:
            classMember = ClassMemberModel()
            classMember.classOn = classOn
            classMember.account = email
            classMember.status = 1
            db.session.add(classMember)
            db.session.commit()
            sendEmailTemplate(email, 'MỜI THAM GIA LỚP HỌC', '/default/mail/moiThamGia.html', accountClass=adminClass,
                              classOn=classOnModel, email=email)
        return jsonify({'data': 'oke'}), 200
    except Exception as e:
        return jsonify({'message': f'{str(e)}'}), 500


def listInvite():
    listClass = ClassMemberModel.query.filter_by(account=current_user.email, status=1)
    return classesMemberSchema.dump(listClass)
