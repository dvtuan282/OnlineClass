from flask import Blueprint, request
import Services.QuizzService as quizzService

quizzRoute = Blueprint('quizzRoute', __name__)


# @quizzRoute.route('/OnlineClass/quizz/<idClass>', methods=['POST'])
# def createQuizz(idClass):
#     return quizzService.createQuizz(idClass)


@quizzRoute.route('/OnlineClass/quizz', methods=['GET'])
def listQuiz():
    return quizzService.listQuizz()


@quizzRoute.route('/OnlineClass/quizz-class/<idClass>', methods=['GET'])
def listQuizInClass(idClass):
    return quizzService.listQuizzInClass(idClass)


@quizzRoute.route('/OnlineClass/quizz-test/<idClass>', methods=['POST'])
def test(idClass):
    data = request.json
    return quizzService.sendMailMember(idClass, data['idQuizz'])


@quizzRoute.route('/test/<idQuizz>', methods=['POST'])
def test1(idQuizz):
    # data = request.files['a']
    return quizzService.createQuizz(idQuizz)
