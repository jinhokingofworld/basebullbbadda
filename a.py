import requests, time
from bs4 import BeautifulSoup
from pymongo import MongoClient

#데이터베이스 연결
uri = "mongodb+srv://gksqkf0824:iIb12ywrv7wlB0BP@kwonsoyun.xkcilez.mongodb.net/?retryWrites=true&w=majority&appName=KWONSOYUN&tlsAllowInvalidCertificates=true"
client = MongoClient(uri, 27017)  # MongoDB는 27017 포트로 돌아갑니다.
db = client.Splint2_Database


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

#결과가 저장될 딕셔너리
doc = {
    "list": resultList,
    "lastUpdatedTime": {
        "time": now
    }
}

#기존 콜렉션 삭제
db.ranking.drop()

# 12개씩 잘라서 딕셔너리로 변환
for i in range(0, 120, 12):
    chunk = texts[i:i + 12]
    if len(chunk) == 12:
        entry = dict(zip(columns, chunk))
        resultList.append(entry)

#DB에 저장
db.ranking.insert_one(doc)

#DB에서 출력
result = db.ranking.find_one({}, {'_id': 0})

print(result)