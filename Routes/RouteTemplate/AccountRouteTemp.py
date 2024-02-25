from flask import Flask, render_template, redirect, Blueprint
from flask_login import login_required, logout_user, current_user
from Services.AccountService import inforAccount

accountTemp_route = Blueprint('accountTemp_route', __name__)


@accountTemp_route.route('/OnlineClass/login', methods=['GET'])
def dang_nhap():
    return render_template('/default/dangNhap.html')


@accountTemp_route.route('/OnlineClass/register-account', methods=['GET'])
def dang_ky():
    return render_template('/default/dangKy.html')


@accountTemp_route.route('/thong-tin', methods=['GET'])
def thong_tin():
    return render_template('/default/thongTin.html', account=current_user)


@accountTemp_route.route('/dang-xuat', methods=['GET'])
@login_required
def dang_xuat():
    logout_user()
    return render_template('default/dangNhap.html')
