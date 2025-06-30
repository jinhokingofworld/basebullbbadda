import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
from flask import Flask, render_template, request, jsonify, session

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
   count = 0

   #데이터구조
   columns = ["순위", "팀명", "경기", "승", "패", "무", "승률", "게임차", "최근10경기", "연속", "홈", "원정"]
   docs = {}
   alist = []

   #기존 콜렉션 삭제
   db.ranking.drop()

   # 12개씩 잘라서 딕셔너리로 변환
   for i in range(0, 120, 12):
      chunk = texts[i:i + 12]
      if len(chunk) == 12:
         doc = dict(zip(columns, chunk))
         alist.append(doc)
         db.ranking.insert_one(doc) #딕셔너리 하나씩 DB에 저장

   #DB에서 데이터 가져오기
   a = list(db.ranking.find({}))
  
   resultList = []
   for i in range(len(a)):
      resultDoc = {
      "순위" : "", 
      "팀명" : "", 
      "경기" : "", 
      "승" : "", 
      "패": "", 
      "무" : "", 
      "승률": ""
      }
      resultDoc['순위'] = a[i]['순위']
      resultDoc['팀명'] = a[i]['팀명']
      resultDoc['경기'] = a[i]['경기']
      resultDoc['승'] = a[i]['승']
      resultDoc['패'] = a[i]['패']
      resultDoc['무'] = a[i]['무']
      resultDoc['승률'] = a[i]['승률']
      resultList.append(resultDoc)
   
   return resultList # scrapRanking() 끝

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
   scrapedRanking = scrapRanking()
   return scrapedRanking

#메인페이지 유저 이미지 요청 처리
@app.route('/api/getUserImg', methods=['GET'])
def getUserImg():
    #세션 아이디 확인
    element = get_session()
    #로그인 상태가 아니면 종료
    if not element['logged_in']:
      return jsonify({'msg': '로그인 상태가 아닙니다.'})
    # 세션과 아이디가 같은 회원의 idol을 반환 //좋아하는 선수 이미지 저장
    target = db.user.find_one({'id': element['id']}, {'_id': 0})
    img = target['idol']
    return jsonify({'msg' : 'success', 'img' : img})

# 메인 페이지 주소
@app.route('/')
def home():
   return render_template('index.html')

teams_col = db.teams  # 이거 꼭 있어야 함

@app.route('/team/<team_id>')
def team_detail(team_id):
    team_name_map = {
        "Tigers": "KIA 타이거즈",
        "Giants": "롯데 자이언츠",
        "Twins": "LG 트윈스",
        "Bears": "두산 베어스",
        "Lions": "삼성 라이온즈",
        "Wiz": "KT 위즈",
        "Eagles": "한화 이글스",
        "Heros": "키움 히어로즈",
        "Dinos": "NC 다이노스",
        "Landers": "SSG 랜더스"
    }

    team_name = team_name_map.get(team_id)
    team_data = teams_col.find_one({"team_name": team_name})

    return render_template("teampage.html", team=team_data)


# 서버 실행
if __name__ == '__main__':
   app.run('0.0.0.0', port=5000)