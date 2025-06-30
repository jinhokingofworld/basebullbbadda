# from flask import Blueprint,render_template

# team_page = Blueprint('team', __name__, static_folder="static", template_folder="templates", url_prefix="/team")
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
from flask import Blueprint, jsonify, request, render_template,session

team_page = Blueprint('team', __name__, static_folder="static", template_folder="templates", url_prefix="/team")

# #팀 페이지 동적 라우팅
# @team_page.route('/<teamName>')
# def routing_myPage(teamName):
#     return render_template('teampage.html', teamName=teamName)
uri = "mongodb+srv://gksqkf0824:iIb12ywrv7wlB0BP@kwonsoyun.xkcilez.mongodb.net/?retryWrites=true&w=majority&appName=KWONSOYUN&tlsAllowInvalidCertificates=true"
client = MongoClient(uri, 27017) #MongoDB는 27017 포트로 돌아갑니다.
db = client.Splint2_Database

#팀 페이지 동적 라우팅
@team_page.route('/<teamName>')
def routing_myPage(teamName):
    return '<h1>' + teamName +'의 teamPage입니다</h1>'


@team_page.route('/<teamName>/comment', methods =['POST'])
def post_comment():

    # 입력받은 Comment 데이터 가져오기
    input_comment = request.form['comment']

    #세션된 ID,닉네임 가져오기
    target_user = session.get('id')
    Nickname = session.get('nickname')

    # DB에 도큐멘트 형태로 변환
    doc = {
        'id' : target_user, 'nickname' : Nickname, 'comment' : input_comment } #좋아요 추가시 user db와 이름혼동문제 
    
    # DB에 아이디, 닉네임과 댓글 내용 데이터 저장
    db.team_comment.insert_one(doc)

    # 댓글 등록 성공 (응답 성공 반환)
    return jsonify( {'result': 'success','msg' : '댓글 등록 성공!', 'nickname' : Nickname, 'url' : '/<teamName>'})
    
    # #id와 nickname을 세션 등록
    # session['id'] = target_user['id']
    # session['nickname'] = nickname
    # return jsonify({'result': 'success', 'msg' : nickname + '님 환영합니다.', 'nickname' : nickname, 'url' : '/'})

    
