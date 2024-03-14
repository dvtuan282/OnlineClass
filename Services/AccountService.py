from flask import jsonify, request, session, url_for, redirect
from Models.AccountModel import AccountModel, accountSchema, accountsSchema
from Utilities.RamdomCode import ramdomCode
from flask_login import login_user, current_user
from Utilities.Config import db, oauth
from Utilities.Email import sendEmailText


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


def authorize():
    token = oauth.google.authorize_access_token()
    resp = oauth.google.get('userinfo')
    resp.raise_for_status()
    profile = resp.json()
    account = AccountModel.query.get(profile['email'])
    if not account:
        accountAdd = AccountModel()
        accountAdd.email = profile['email']
        accountAdd.password = ramdomCode()
        accountAdd.name = profile['name']
        accountAdd.avatar = profile['picture']
        db.session.add(accountAdd)
        db.session.commit()
        login_user(accountAdd)
    else:
        login_user(account)
    return redirect('http://127.0.0.1:5000/OnlineClass/home')


def googleLogin():
    google = oauth.create_client('google')
    # Sử dụng callback URL chính xác đã được đăng ký với Google OAuth
    redirect_uri = url_for('accountTemp_route.authorize', _external=True)
    return google.authorize_redirect(redirect_uri)
