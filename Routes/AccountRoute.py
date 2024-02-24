from flask import Blueprint, jsonify
import Services.AccountService as accountService
from flask_login import login_required, logout_user

accountRoute = Blueprint('accountRouter', __name__)


@accountRoute.route('/OnlineClass/register-account', methods=['POST'])
def registerAccount():
    return accountService.registerAccount()


@accountRoute.route('/OnlineClass/send-Verification-code/<email>', methods=['POST'])
def send_code_confirm(email):
    return accountService.sendVerificationCode(email)


@accountRoute.route('/OnlineClass/forgot-password/<email>', methods=['POST'])
def forgot_password(email):
    return accountService.forgotPassword(email)


@accountRoute.route('/OnlineClass/information', methods=['GET'])
@login_required
def account_information():
    return accountService.inforAccount()


@accountRoute.route('/OnlineClass/logout', methods=['GET'])
@login_required
def logout():
    return logout_user()


@accountRoute.route('/OnlineClass/login', methods=['POST'])
def login_account():
    return accountService.loginAccount()

