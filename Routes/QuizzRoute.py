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


@quizzRoute.route('/OnlineClass/quizz/<idQuizz>', methods=['GET'])
def informationQuizz(idQuizz):
    return quizzService.informationQuizz(idQuizz)


@quizzRoute.route('/OnlineClass/quizz/<idQuizz>', methods=['POST'])
def createQuizz(idQuizz):
    # data = request.files['a']
    return quizzService.createQuizz(idQuizz)


@quizzRoute.route('/OnlineClass/quizz-question/<idQuizz>', methods=['GET'])
def showQuestion(idQuizz):
    return quizzService.showQuestionAndAnswer(idQuizz)
