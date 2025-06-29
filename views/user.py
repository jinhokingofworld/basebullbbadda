import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
from flask import Blueprint, jsonify, request, render_template

user_page = Blueprint('user', __name__, static_folder="static", template_folder="templates", url_prefix="/user")

uri = "mongodb+srv://gksqkf0824:iIb12ywrv7wlB0BP@kwonsoyun.xkcilez.mongodb.net/?retryWrites=true&w=majority&appName=KWONSOYUN&tlsAllowInvalidCertificates=true"
client = MongoClient(uri, 27017) #MongoDB는 27017 포트로 돌아갑니다.
db = client.user


 # MongoDB에 insert 하기
    
# 'users'라는 collection에 {'ID':'myungwan31','PW':jungleFighting}를 넣습니다.
# db.users.insert_one({'ID':'myungwan31','PW':'jungleFighting'})






@user_page.route('/')
def read_users():
    return render_template('login.html')
    

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