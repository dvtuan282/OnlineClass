from datetime import datetime

from sqlalchemy import desc

from Models.PostModel import postsSchema, postSchema, PostModel
from flask import request, jsonify
from flask_login import current_user
from Utilities.Config import db


def createPost():
    data = request.json
    try:
        data['account'] = current_user.email
        data['datePosted'] = datetime.now()
        post = postSchema.load(data)
        db.session.add(post)
        db.session.commit()
        return jsonify({'message': 'Post an article successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'{str(e)}'})


def deletePost(id):
    try:
        post = PostModel.query.get(id)
        db.session.delete(post)
        db.session.commit()
        return jsonify({'message': 'Delete a post successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'{str(e)}'})


def listPostInClass(idClass):
    posts = PostModel.query.filter_by(classOn=idClass).order_by(desc(PostModel.datePosted)).all()
    return jsonify(postsSchema.dump(posts))

def informationPost(idPost):
    post = PostModel.query.get(idPost)
    return jsonify(postSchema.dump(post))


def editPost(idPost):
    data = request.json
    post = PostModel.query.get(idPost)
    try:
        post.content = data['content']
        db.session.commit()
        return jsonify({'message': 'Update a post successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Update post unsuccessful'})
