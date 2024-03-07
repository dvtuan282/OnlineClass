from flask import Blueprint
import Services.PostService as postService

postRoute = Blueprint('postRoute', __name__)


@postRoute.route('/OnlineClass/create-post', methods=['POST'])
def createPost():
    return postService.createPost()


@postRoute.route('/OnlineClass/list-post-in-class/<idClass>', methods=['GET'])
def listPostInClass(idClass):
    return postService.listPostInClass(idClass)


@postRoute.route('/OnlineClass/update-post/<idClass>', methods=['PUT'])
def editPost(idClass):
    return postService.editPost(idClass)


@postRoute.route('/OnlineClass/delete-post/<idClass>', methods=['DELETE'])
def deletePost(idClass):
    return postService.deletePost(idClass)


# @postRoute.route('/OnlineClass/information-post/<idPost>', methods=['GET'])
# def informationPost(idPost):
#     return postService.informationPost(idPost)

# @postRoute.route('/test/<idPost>', methods=['GET'])
# def test(idPost):
#         return postService.test(idPost)
