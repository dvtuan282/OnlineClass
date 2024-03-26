from flask import Blueprint
import Services.ClassMemberService as classMemberService

classMemberRoute = Blueprint('classMemberRoute', __name__)


@classMemberRoute.route('/OnlineClass/member/<idClass>', methods=['GET'])
def listMemberInClass(idClass):
    return classMemberService.showMemberInClass(idClass)


@classMemberRoute.route('/OnlineClass/member', methods=['POST'])
def createMemberInClass():
    return classMemberService.createMemberInClass()


@classMemberRoute.route('/OnlineClass/member/<idClass>', methods=['PUT'])
def confirmJoinClass(idClass):
    return classMemberService.confirmJoinClass(idClass)


@classMemberRoute.route('/OnlineClass/member/<idClassMember>', methods=['DELETE'])
def deleteMemberInClass(idClassMember):
    return classMemberService.deleteMember(idClassMember)


@classMemberRoute.route('/OnlineClass/listInvitation', methods=['GET'])
def listInvitation():
    return classMemberService.listInvite()


@classMemberRoute.route('/OnlineClass/create-members/<idClass>', methods=['POST'])
def createMembers(idClass):
    return classMemberService.createMembersInClass(idClass)


@classMemberRoute.route('/OnlineClass/member1/<idClass>', methods=['PUT'])
def confirmJoinClass1(idClass):
    return classMemberService.confirmJoinClass(idClass)
