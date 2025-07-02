import requests, time, copy
from bs4 import BeautifulSoup
from pymongo import MongoClient
from flask import Flask, render_template, jsonify, session

app = Flask(__name__)
from views import create_app
create_app(app)

#데이터베이스 연결
uri = "mongodb+srv://gksqkf0824:iIb12ywrv7wlB0BP@kwonsoyun.xkcilez.mongodb.net/?retryWrites=true&w=majority&appName=KWONSOYUN&tlsAllowInvalidCertificates=true"
client = MongoClient(uri, 27017)  # MongoDB는 27017 포트로 돌아갑니다.
db = client.Splint2_Database

def scrapRanking():
    # 타겟 URL을 읽어서 HTML를 받아오고,
    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get('https://www.koreabaseball.com/Record/TeamRank/TeamRank.aspx', headers=headers)

    # HTML을 BeautifulSoup이라는 라이브러리를 활용해 검색하기 용이한 상태로 만듦
    # soup이라는 변수에 "파싱 용이해진 html"이 담긴 상태가 됨
    # 이제 코딩을 통해 필요한 부분을 추출하면 된다.
    soup = BeautifulSoup(data.text, 'html.parser')

    td_elements = soup.select('#cphContents_cphContents_cphContents_udpRecord .tData tbody tr td')
    texts = [td.get_text(strip=True) for td in td_elements]

    #데이터구조
    columns = ["순위", "팀명", "경기", "승", "패", "무", "승률", "게임차", "최근10경기", "연속", "홈", "원정"]
    resultList = []
    now = time.time()

    #결과가 저장될 형식
    doc = {
        "list": resultList,
        "lastUpdatedTime": now
    }

    # 12개씩 잘라서 딕셔너리로 변환
    for i in range(0, 120, 12):
        chunk = texts[i:i + 12]
        if len(chunk) == 12:
            entry = dict(zip(columns, chunk))
            resultList.append(entry)

    #DB에 저장
    db.ranking.replace_one({}, doc, upsert=True)
    
    #DB에서 출력
    result = db.ranking.find_one({}, {'_id': 0})

    return result # scrapRanking() 끝

#세션 확인하는 API
@app.route('/api/session', methods = ['GET'])
def get_session():
    if 'id' in session: #session은 리스트 형태
        return jsonify({'logged_in': True, 'id': session['id'], 'nickname': session['nickname']})
    else:
        return jsonify({'logged_in': False, 'msg' : '로그인상태가 아닙니다.', 'url': '/user/login'})

#팀 순위 api 요청에 응답
@app.route('/api/ranking')
def getRanking():
    # #현재 시간 확인
    now = time.time()
    #DB에서 마지막으로 저장한 시간 lastUpdatedTime 찾아서 현재와 비교
    target = db.ranking.find_one()
    lastUpdatedTime = float(target['lastUpdatedTime'])
    #10분 이상 지났으면,
    if (now - lastUpdatedTime) >= 600:
        #새로 스크랩 해오기
        result = scrapRanking()
    else:
        #DB에 저장된 랭킹 불러오기
        result = db.ranking.find_one({}, {'_id': 0})

    return jsonify(result)

#메인페이지 유저 이미지 요청 처리
@app.route('/api/getUserImg', methods=['GET'])
def getUserImg():
    #세션 아이디 확인
    user_id = session.get('id')
   
    #로그인 상태가 아니면 종료
    if not user_id:
      return jsonify({'msg': '로그인 상태가 아닙니다.'})
    
    # 세션과 아이디가 같은 회원의 idol을 반환 //좋아하는 선수 이미지 저장
    # DB에서 해당 ID를 가진 유저 조회
    user = db.user.find_one({'id': user_id}, {'_id': 0})
    if not user:
        return jsonify({'msg': '해당 유저가 존재하지 않습니다.'})
    # idol 필드가 있는지 확인
    if 'idol' not in user:
        return jsonify({'msg': '프로필 이미지가 없습니다.'})
    # 정상 반환
    return jsonify({'msg': 'success', 'img': user['idol']})

# 메인 페이지 주소
@app.route('/')
def home():
   return render_template('index.html')

teams_col = db.teams  # 이거 꼭 있어야 함

# #팀별 페이지로 라우팅
# @app.route('/team/<team_id>')
# def team_detail(team_id):
#     team_name_map = {
#         "Tigers": "KIA 타이거즈",
#         "Giants": "롯데 자이언츠",
#         "Twins": "LG 트윈스",
#         "Bears": "두산 베어스",
#         "Lions": "삼성 라이온즈",
#         "Wiz": "KT 위즈",
#         "Eagles": "한화 이글스",
#         "Heros": "키움 히어로즈",
#         "Dinos": "NC 다이노스",
#         "Landers": "SSG 랜더스"
#     }

#     team_name = team_name_map.get(team_id)
#     team_data = teams_col.find_one({"team_name": team_name})

#     return render_template("teampage.html", team=team_data,team_id = team_id)

player_db = {
    "KIA_TIGERS": "kia_player",
    "LOTTE_GIANTS": "lotte_player",
    "LG_TWINS": "lg_player",
    "DOOSAN_BEARS": "dosan_player",
    "SAMSUNG_LIONS": "samsung_player",
    "KT_WIZ": "kt_player",
    "KIWOOM_HEROS": "kiwoom_player",
    "NC_DIONS": "nc_player",
    "SSG_LANDERS": "ssg_player",
    "HANWHA_EAGLES" : "hanwha_player"
}

#팀별 선수 DB객체 출력
@app.route('/players/api/<teamName>')
def showPlayerList(teamName):

    #시간 확인하고 스크래핑하는 코드 나중에 추가
    
    #컬렉션 이름 가져오기
    collection_name = player_db[teamName]
    #컬렉션 접근
    collection = db[collection_name]
    #DB에서 데이터 불러오기
    targets = collection.find({}, {'_id': 0, 'name' : 1, 'img' : 1, 'playerId' : 1})
    #리스트에 넣어서 DB 전체 전달하기
    resultList = list(targets)
    #응답 전달
    return jsonify(resultList)


#선수 리스트 페이지로 라우팅
@app.route('/playerlist')
def showList():
    return render_template('playerlist.html')

# 서버 실행
if __name__ == '__main__':
   app.run('0.0.0.0', port=5000, debug=True)