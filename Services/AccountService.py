import requests
from flask import jsonify, request, session, url_for, redirect
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

from Models.AccountModel import AccountModel, accountSchema, accountsSchema
from Utilities.RamdomCode import ramdomCode
from flask_login import login_user, current_user
from Utilities.Config import db
from Utilities.Email import sendEmailText
import Services.DaoService as daoService


def loginAccount():
    data = request.json
    account = AccountModel.query.get(data['email'])
    if account:
        if account.password == data['password']:
            """
            Hàm login_user() nhận vào đối tượng user để lưu người dùng vào phiên làm việc 
            có các thêm các tham số(tự tìm hiểu)
            """
            login_user(account)
            return jsonify({"message": "Login in successfully"})
        else:
            return jsonify({"message": "Incorrect password"})
    else:
        return jsonify({"message": "Login unsuccessful"})


def registerAccount():
    data = request.json
    verificationCode = session.get('verificationCode')
    if data['verificationCode'] != verificationCode:
        return jsonify({'message': 'Incorrect verification code'})

    try:
        data.pop('verificationCode')
        account = accountSchema.load(data)
        db.session.add(account)
        db.session.commit()
        session.pop('verificationCode')
        return jsonify({'message': 'register successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'{str(e)}'})


def sendVerificationCode(email):
    try:
        if len(email) > 0:
            code = ramdomCode()
            session['verificationCode'] = code
            subject = 'Mã xác nhận đăng ký tài khoản OnlineClass'
            content = 'Đây là mã xác nhận đăng ký tài khoản của bạn: ' + session['verificationCode']
            sendEmailText(email, subject, content)
            return jsonify({'message': 'send verification code succussfully'})
        else:
            return jsonify({'message': 'please endter email'})
    except Exception as e:
        return jsonify({'message': f'{str(e)}'})


def forgotPassword(email):
    newPassword = ramdomCode()
    try:
        account = AccountModel.query.get(email)
        account.password = newPassword
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'{str(e)}'})
    subject = 'Cấp lại mật khẩu'
    content = 'Mật khẩu mới của bạn là: ' + newPassword
    sendEmailText(email, subject, content)
    return jsonify({'message': 'reissue password successfully'})


def listAccount():
    return accountsSchema.dump(AccountModel.query.all())


def inforAccount():
    return current_user
