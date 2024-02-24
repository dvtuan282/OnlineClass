from datetime import datetime

from flask import jsonify, request
from Models.CommentModel import CommentModel, commentsSchema, commentSchema
from flask_login import current_user
from Utilities.Config import db


def createComment(idPost):
    try:
        data = request.json
        data['account'] = current_user.email
        data['dateComment'] = datetime.now()
        data['post'] = idPost
        comment = commentSchema.load(data)
        db.session.add(comment)
        db.session.commit()
        print('a')
        return jsonify({'message': 'Comment successfully'}), 200
    except Exception as e:
        db.session.rollback()
        print('b')
        return jsonify({'message': f'{str(e)}'})


def deleteComment(idCmt):
    try:
        comment = CommentModel.query.get(idCmt)
        db.session.delete(comment)
        db.session.commit()
        return jsonify({'message': 'Deleted comment successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'{str(e)}'})


def editComment(idCmt):
    try:
        data = request.json
        comment = CommentModel.query.get(idCmt)
        comment.content = data['contentCmt']
        db.session.commit()
        return jsonify({'message': 'Edited comment successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'{str(e)}'})
