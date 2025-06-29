import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
from flask import Blueprint, jsonify, request, render_template

user_page = Blueprint('user', __name__, static_folder="static", template_folder="templates", url_prefix="/user")

uri = "mongodb+srv://gksqkf0824:iIb12ywrv7wlB0BP@kwonsoyun.xkcilez.mongodb.net/?retryWrites=true&w=majority&appName=KWONSOYUN&tlsAllowInvalidCertificates=true"
client = MongoClient(uri, 27017) #MongoDB는 27017 포트로 돌아갑니다.
db = client.Splint2_Database


 # MongoDB에 insert 하기
    
# 'users'라는 collection에 {'ID':'myungwan31','PW':jungleFighting}를 넣습니다.
# db.users.insert_one({'ID':'myungwan31','PW':'jungleFighting'})


# 회원가입 api 응답하는 부분
@user_page.route('/api/signin', methods=['POST'])
def read_users():
    # DB에 ID,PW,nickname 데이터 저장
    ID = request.form['id']
    PW = request.form['pw']
    Nickname =request.form['nickname']
    
    #DB에 중복여부 체크후 중복시 메세지 반환후 종료
    IDcheck = db.user.find_one({'id': ID})
    if ID == IDcheck:
        return jsonify({'msg' : '중복된 아이디입니다.','id' : ID})
    
    


    # DB에 도큐먼트 형태로 변환
    doc = { 'id' : ID, 'pw': PW, 'nickname': Nickname, 'idol' :'', 'likes': [] }
    # DB에 저장       
    db.user.insert_one(doc)

    # 가입 성공
    return jsonify({'msg' :'회원가입 성공하셨습니다.', 'nickname' : Nickname , 'url' : '/'})
    

# 로그인 페이지 라우팅
@user_page.route('/')
def routing_users():
    return render_template('signin.html')
    

# @user_page.route('/signin', methods=['POST'])
# def read_users():
#     print(" 요청받음")
#     # user_ID = request.args.get("user")
#     # print(user_ID)
#     print("요청했음")
#     return jsonify({"result : s"})
    
    

# @user_page.route('/',methods=['POST'])
# def login_users():
#     print("요청보냄")
#     # user_ID= request.args.get("user")
#     # print(user_ID)

#     data = request.get_json()
#     user_id = data.get('id')
#     user_pw = data.get('pw')
#     print("받은 ID: {user_id}, PW: {user_pw}")

#     user = db.users.find_one({"ID": user_id})  # ID로 사용자 찾기

#     if user:
#         if user["PW"] == user_pw:
#             return jsonify({'result': 'success', 'msg': '로그인 성공'})
#         else:
#             return jsonify({'result': 'fail', 'msg': '로그인 실패'})

#     else:
#         return jsonify({'result': 'success', 'msg': 'POST 연결되었습니다!'})