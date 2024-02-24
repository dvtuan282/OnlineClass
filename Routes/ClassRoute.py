from flask import Flask, Blueprint
import Services.ClassService as classService

classRoute = Blueprint('classRoute', __name__)


@classRoute.route('/OnlineClass/list-class-of-account', methods=["GET"])
def listClassOfAccount():
    return classService.listClassOfAccount()


@classRoute.route('/OnlineClass/list-of-class-involved', methods=["GET"])
def listOfClassInvolved():
    return classService.listOfClassInvolved()


@classRoute.route('/OnlineClass/create-class', methods=["POST"])
def createClass():
    return classService.createClass()


@classRoute.route('/OnlineClass/informationClass/<idClass>', methods=['GET'])
def informationClass(idClass):
    return classService.informationClass(idClass)
