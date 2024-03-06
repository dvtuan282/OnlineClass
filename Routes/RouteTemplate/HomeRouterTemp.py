from flask import Flask, render_template, redirect, Blueprint
from flask_login import login_required
from Services.AccountService import listAccount
from Services.ClassService import listClassOfAccountObject

homeRouteTemp = Blueprint('homeRouteTemp', __name__)


@homeRouteTemp.route('/OnlineClass/home', methods=["GET"])
@login_required
def home():
    return render_template('default/trangChu.html')


@homeRouteTemp.route('/OnlineClass/class/<idClass>', methods=["GET"])
@login_required
def detailsClass(idClass):
    return render_template('default/lop.html', listAccount=listAccount(), listClass=listClassOfAccountObject())


@homeRouteTemp.route('/OnlineClass/list-invitation', methods=["GET"])
@login_required
def listInvitation():
    return render_template('default/moiThamGia.html')
