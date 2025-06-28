import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
from flask import Blueprint, jsonify, request


uri = "mongodb+srv://gksqkf0824:iIb12ywrv7wlB0BP@kwonsoyun.xkcilez.mongodb.net/?retryWrites=true&w=majority&appName=KWONSOYUN&tlsAllowInvalidCertificates=true"
client = MongoClient(uri, 27017) #MongoDB는 27017 포트로 돌아갑니다.
db = client.user





bp = Blueprint('user', __name__, url_prefix='/user')


@bp.route('/', methods=['GET'])
def read_users():
    print(" 요청받음")
    user_ID = request.args.get("user")
    print(user_ID)

    return jsonify({"result : s"})
    # result = db.jungleUser.find_one({"ID":})
    # if (result가 db내 존재한다면) {
    #     return jsonify({'result':'success', 'msg':'POST 연결되었습니다!'})
    # }    
    # 2. input-ID라는 키 값으로 ID 정보 보내주기
    