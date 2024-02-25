from flask import request, jsonify
from flask_login import current_user

from Models.ClassMemberModel import classesMemberSchema, classMemberSchema, ClassMemberModel
from Models.ClassModel import ClassModel
from Utilities.Config import db
from Models.AccountModel import AccountModel
from Utilities.Email import sendEmailTemplate


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


def listInvite():
    listClass = ClassMemberModel.query.filter_by(account=current_user.email, status=1)
    return classesMemberSchema.dump(listClass)
