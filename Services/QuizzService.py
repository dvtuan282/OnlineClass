from builtins import quit, print
from datetime import datetime
import pandas as pd
from flask import jsonify, request
from sqlalchemy.dialects.mysql import json
from Models.AnswerModel import AnswerModel
from Models.QuestionModel import QuestionModel
from Models.QuizzModel import QuizzModel, quizzSchema, quizzesSchema
from Models.quizzClassModel import QuizzClassModel
from Utilities.Config import db
from Utilities.RamdomCode import ramdomCode
from Utilities.Email import sendEmailTemplate
from Models.ClassMemberModel import ClassMemberModel
from flask_login import current_user


def createQuizz(idClass):
    try:
        file_question = request.files['fileQuestion']
        title = request.form['title']
        open_time = request.form['openTime']
        # print("a", open_time)
        closed_time = request.form['closedTime']
        test_time = request.form['testTime']
        list_class_share = request.form['listClassShare']
        idQuizz = ramdomCode()
        # Lấy status theo openTime và closedTime thêo hàm statusTest
        status = statusTest(open_time, closed_time)
        ''' Lấy danh sách các lớp được tạo cùng với bài kiểm tra, 
        thực hiện lưu vào listClass khi xong thì pop listClassShate đi'''
        listClass = [i for i in list_class_share]
        listClass.append(idClass)
        # Lưu db
        data = QuizzModel(id=idQuizz, title=title, openTime=open_time, closedTime=closed_time, testTime=test_time,
                          status=1)
        db.session.add(data)
        db.session.commit()
        # Tạo câu hỏi và câu trả lời bằng file Excel
        creatQuestionAndAnswerFile(file_question, idQuizz)
        # Tạo dữ liệu cho bảng trung gian
        createQuizzClas(idClass, data.id)
        # Send Mail
        sendMailMember(idClass, data.id)
        return jsonify({'message': 'create quizz successfully'}), 200
    except Exception as e:
        # db.session.rollback()
        return jsonify({'message': f'{str(e)}'}), 500


def listQuizz():
    listA = QuizzModel.query.all()
    return quizzesSchema.dump(listA)


def listQuizzInClass(idClass):
    quizzClass = QuizzClassModel.query.filter_by(classOn=idClass).all()
    quizzInClass = [quizz.quizz_quizzClass for quizz in quizzClass]
    return jsonify(quizzesSchema.dump(quizzInClass))


def createQuizzClas(listClass, idQuizz):
    try:
        for i in listClass:
            quizzClass = QuizzClassModel()
            quizzClass.quizz = idQuizz
            quizzClass.classOn = i
            db.session.add(quizzClass)
            db.session.commit()
        return jsonify({"message": "Create quizzClass successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f'{str(e)}'})


def statusTest(openTime, closedTime):
    current = datetime.now()
    openTimeCv = datetime.strptime(openTime, "%Y-%m-%dT%H:%M:%S")
    closedTimeCv = datetime.strptime(closedTime, "%Y-%m-%dT%H:%M:%S")
    if openTimeCv > current or closedTimeCv <= current:
        # Đóng
        return 1
    else:
        # Mở
        return 0


def sendMailMember(idClass, idQuizz):
    listMember = ClassMemberModel.query.filter_by(classOn=idClass).all()
    quizz = QuizzModel.query.get(idQuizz)
    currentDate = datetime.now()
    for i in listMember:
        if i.status == 0:
            sendEmailTemplate(i.account, 'THÔNG BÁO ĐĂNG BÀI TẬP MỚI', '/default/mail/ThongBaoBaiTapMoi.html',
                              quizz=quizz, nguoiTao=current_user.name, currentDate=currentDate)

    return jsonify({'mess': 'oke'})


def autoUpdateStatus():
    pass


def creatQuestionAndAnswerFile(file_path, quizz):
    df = pd.read_excel(file_path)
    for index, row in df.iterrows():
        question = createQuestion(row["Câu hỏi"], quizz)
        for columnName, columnValue in row.items():
            if columnName.startswith("Đáp án"):
                isCorrect = 1 if columnName == "Đáp án đúng" else 0
                answer = AnswerModel(id=0, title=columnValue, isCorrect=isCorrect, question=question.id)
                createAnswer(answer)
    return jsonify({'oke': 'k'})


def createQuestion(titleQuestion, quizz):
    questionModel = QuestionModel()
    questionModel.title = titleQuestion
    questionModel.quizz = quizz
    db.session.add(questionModel)
    db.session.commit()
    return questionModel


def createAnswer(answer):
    try:
        db.session.add(answer)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
