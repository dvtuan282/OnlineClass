from flask import jsonify, request
from Models.ResultsModel import manyResultsSchema, resultsSchema, ResultsModel, db
from flask_login import current_user


def createResults(quizz):
    listResultsData = request.json
    for re in listResultsData:
        re["account"] = current_user.email
        re["quizz"] = quizz
        results = resultsSchema.load(re)
        db.session.add(results)
        db.session.commit()
    return jsonify(listResults(quizz))


def listResults(quizz):
    results = ResultsModel.query.filter_by(quizz=quizz, account=current_user.email).all()
    return manyResultsSchema.dump(results)


def listResultsAll():
    results = ResultsModel.query.all()
    return jsonify(manyResultsSchema.dump(results))
