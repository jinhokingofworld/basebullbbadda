import requests
from bs4 import BeautifulSoup
from flask import Blueprint, jsonify, request, render_template,session
from db_config import db


user_page = Blueprint('user', __name__, static_folder="static", template_folder="templates", url_prefix="/user")


# 회원가입 api 응답하는 부분
@user_page.route('/api/signup', methods=['POST'])
def read_users():
    
    # 입력값 ID,PW,nickname 데이터 추출
    ID = request.form['id']
    PW = request.form['pw']
    PWchk = request.form['pwchk']
    Nickname =request.form['nickname']
    
    if ID == "" or PW =="":
        return jsonify({'result': 'fail','msg' : "아이디와 비밀번호를 입력하세요"})
    
    if PW != PWchk :
        return jsonify({'result': 'fail','msg' : "패스워드가 일치하지 않습니다"})

    if Nickname == "":
        return jsonify({'result': 'fail','msg' : "닉네임을 입력하세요"})

    #DB에 중복여부 체크후 중복시 응답실패 반환
    IDcheck = db.user.find_one({'id': ID})
    if IDcheck:
        return jsonify({'result': 'fail','msg' : '중복된 아이디입니다.','id' : ID})

    # DB에 도큐먼트 형태로 변환
    doc = { 'id' : ID, 'pw': PW, 'nickname': Nickname, 'idol' :'', 'likes': [] }
    # DB에 저장       
    db.user.insert_one(doc)

    # 가입 성공 (응답 성공 반환)
    return jsonify({'result': 'success','msg' :'회원가입 성공!', 'nickname' : Nickname , 'url' : '/'})
    
#회원 탈퇴 api 응답
@user_page.route('/api/deleteUser', methods=['GET'])
def delete_users():
    # DB에 ID,PW,nickname 데이터 저장
    ID = request.form['id']
    PW = request.form['pw']
    Nickname =request.form['nickname']
    
    #DB에 중복여부 체크후 중복시 응답실패 반환
    IDcheck = db.user.find_one({'id': ID})
    if IDcheck:
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

    #가져온 ID 존재여부 확인 -> ID 없을시 응답실패 반환
    if not target_user:
         return jsonify({'result':'fail','msg' : ' 회원정보가 올바르지 않습니다.','id' : input_ID})
    
    #해당 ID의 닉네임 가져오기
    nickname = target_user.get('nickname')

    # 비번 일치여부 확인 -> 불일치시 응답실패 반환
    if target_user['pw'] !=input_PW:
        return jsonify({'result':'fail','msg' : ' 회원정보가 올바르지 않습니다.','id' : input_ID})
    
    # 가져온 정보 일치시 로그인 성공 & 응답 성공 반환
    #id와 nickname을 세션 등록
    session['id'] = target_user['id']
    session['nickname'] = nickname
    return jsonify({'result': 'success', 'msg' : f'{nickname}님 환영합니다.', 'nickname' : nickname, 'url' : '/'})

#닉네임변경 api 응답
@user_page.route('/api/updateNick', methods=['POST'])
def chg_nick():
    oldId = session.get('id') #기존 아이디
    new = request.form['newNick'] #새 닉네임
    print(id, new)
    db.user.update_one({'id' : oldId}, {'$set':{'nickname': new}})
    session['nickname'] = new
    return jsonify({'result': 'success', 'msg': '닉네임이 변경 되었습니다.', 'nickname': new})

#로그아웃 api 응답하는 부분
@user_page.route('/api/logout', methods=['GET', 'POST'])
def out_users():
    session.clear()  # 세션 전체 삭제
    return jsonify({'result': 'success', 'msg': '로그아웃 되었습니다.'})

#회원탈퇴 api 응답
@user_page.route('/api/delete', methods=['POST'])
def del_users():
    id = request.form.get('id')
    session.clear() # 세션 전체 삭제
    db.user.delete_one({'id': id}) #계정 삭제
    return jsonify({'result': 'success', 'msg': '계정이 삭제 되었습니다.'})

#좋아하는 팀 api 응답하는 부분
@user_page.route('/api/idol', methods=['POST'])
def chg_pic():
    id = session.get('id') #기존 아이디
    team_name = request.form.get('idol')
    #좋아하는 팀의 이름으로 데이터베이스 검색
    targetTeam = db.teams.find_one({'team_name': team_name})
    #이미지 파일 추출
    teamImg = targetTeam['team_image']
    #유저DB에 저장
    db.user.update_one({'id' : id} , {'$set':{'idol': teamImg}})
    return jsonify({'result': 'success', 'msg': f"{targetTeam['team_name']}이 좋아하는 팀으로 등록 되었습니다."})

#좋아하는 기사 저장 api 응답
@user_page.route('/api/likes', methods=['POST'])
def inputLikes():
    URL = request.form['URL']
    ID = session.get('id')
    #받은 URL 기사 스크랩
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(URL, headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')

    article = soup.select_one('.content01 .sub-content .view')

    aTitle = article.select_one('.title>h4>span').text
    aImg = article.select_one('.detail>.img>img')
    imgSrc = 'https:' + aImg['src']

    aDescription = article.select_one('.detail > p:nth-of-type(2)').text

    doc = {
        'title' : aTitle,
        'description' : aDescription,
        'url' : URL,
        'img' : imgSrc
    }

    #DB에 저장
    db.user.update_one({'id': ID}, {'$push': {'likes' : doc}})

    return jsonify({'msg': '즐겨찾기 저장에 성공했습니다.'})

#좋아하는 기사 출력 api 응답
@user_page.route('/api/getLikes')
def getLikes():
    user_id = session.get('id')
    elements = db.user.find_one({'id' : user_id}, {'_id': 0})
    return jsonify(elements)

# 마이 페이지 동적 라우팅
@user_page.route('/<id>')
def routing_myPage(id):
    my_data=db.user.find_one({'id' : id})
    return render_template('myPage.html', MyData = my_data)

# 로그인 페이지 라우팅
@user_page.route('/login')
def routing_login():
    return render_template('login.html')    
