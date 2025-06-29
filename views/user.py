import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
from flask import Blueprint, jsonify, request, render_template,session


user_page = Blueprint('user', __name__, static_folder="static", template_folder="templates", url_prefix="/user")

uri = "mongodb+srv://gksqkf0824:iIb12ywrv7wlB0BP@kwonsoyun.xkcilez.mongodb.net/?retryWrites=true&w=majority&appName=KWONSOYUN&tlsAllowInvalidCertificates=true"
client = MongoClient(uri, 27017) #MongoDB는 27017 포트로 돌아갑니다.
db = client.Splint2_Database


# 회원가입 api 응답하는 부분
@user_page.route('/api/signup', methods=['POST'])
def read_users():
    # DB에 ID,PW,nickname 데이터 저장
    ID = request.form['id']
    PW = request.form['pw']
    Nickname =request.form['nickname']
    
    #DB에 중복여부 체크후 중복시 응답실패 반환
    IDcheck = db.user.find_one({'id': ID})
    if ID == IDcheck ['id']:
        return jsonify({'result': 'fail','msg' : '중복된 아이디입니다.','id' : ID})

    


    # DB에 도큐먼트 형태로 변환
    doc = { 'id' : ID, 'pw': PW, 'nickname': Nickname, 'idol' :'', 'likes': [] }
    # DB에 저장       
    db.user.insert_one(doc)

    # 가입 성공 (응답 성공 반환)
    return jsonify({'result': 'success','msg' :'회원가입 성공!', 'nickname' : Nickname , 'url' : '/'})
    

# 회원가입 페이지 라우팅
@user_page.route('/signup')
def routing_signup():
    return render_template('signup.html')
    

 #로그인 api 응답하는 부분
@user_page.route('/api/login', methods=['POST'])
def bring_users():
    
    # 입력받은 ID,PW 데이터 가져오기
    input_ID = request.form['id']
    input_PW = request.form['pw']

    #DB에서 ID 가져오기
    target_user = db.user.find_one({'id': input_ID})

    #해당 ID의 닉네임 가져오기
    nickname = target_user.get('nickname')

    # 가져온 ID 존재여부와 비번 일치여부 확인 -> 불일치시 응답실패 반환
    if not target_user or target_user['pw'] !=input_PW:
        return jsonify({'result':'fail','msg' : ' 회원정보가 올바르지 않습니다.','id' : input_ID})
    
    # 가져온 정보 일치시 로그인 성공 & 응답 성공 반환
    #세션 등록
    session['id'] = target_user['id']
    return jsonify({'result': 'success', 'msg' : nickname + '님 환영합니다.', 'nickname' : nickname, 'url' : '/'})

#로그아웃 api 응답하는 부분
@user_page.route('/api/logout', methods=['GET','POST'])
def out_users():
    session['id'] = ""
    

# 로그인 페이지 라우팅
@user_page.route('/login')
def routing_login():
    return render_template('login.html')    

