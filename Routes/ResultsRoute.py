from flask import Blueprint
import Services.ResultsService as resultsService

resultsRoute = Blueprint('resultsRoute', __name__)


@resultsRoute.route('/OnlineClass/results/<quizz>', methods=['POST'])
def createResults(quizz):
    return resultsService.createResults(quizz)


@resultsRoute.route('/test')
def test():
    return resultsService.listResultsAll()
