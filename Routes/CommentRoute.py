from flask import Blueprint
import Services.CommentService as commentService

commentRoute = Blueprint('commentRoute', __name__)


@commentRoute.route('/OnlineClass/comment/<idPost>', methods=['POST'])
def createComment(idPost):
    return commentService.createComment(idPost)


@commentRoute.route('/OnlineClass/comment/<idCmt>', methods=['DELETE'])
def deleteComment(idCmt):
    return commentService.deleteComment(idCmt)


@commentRoute.route('/OnlineClass/comment/<idCmt>', methods=['PUT'])
def editComment(idCmt):
    return commentService.editComment(idCmt)
