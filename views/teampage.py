import os, unicodedata
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"        # TensorFlow 로그 제거
os.environ["DISABLE_TFLITE_DELEGATE"] = "1" 
import requests, time
from bs4 import BeautifulSoup
from pymongo import MongoClient
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
from flask import Flask, Blueprint, render_template, jsonify,request,session
from datetime import datetime
from . import player

team_page = Blueprint('team', __name__, static_folder="static", template_folder="templates", url_prefix="/team")

uri="mongodb+srv://gksqkf0824:iIb12ywrv7wlB0BP@kwonsoyun.xkcilez.mongodb.net/?retryWrites=true&w=majority&appName=KWONSOYUN&tlsAllowInvalidCertificates=true"
client=MongoClient("mongodb+srv://gksqkf0824:iIb12ywrv7wlB0BP@kwonsoyun.xkcilez.mongodb.net/?retryWrites=true&w=majority&appName=KWONSOYUN&tlsAllowInvalidCertificates=true")
db=client.Splint2_Database
teams_col=db.teams

options=Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shu-usage')


driver=webdriver.Chrome(options=options)

#팀 홈페이지 정보
team_homepage={
     "KIA 타이거즈": "https://tigers.co.kr/",
     "롯데 자이언츠": "https://www.giantsclub.com/html/",
     "LG 트윈스": "https://www.lgtwins.com/service/html.ncd?view=/pc_twins/twins_main/twins_main",
     "두산 베어스": "https://www.doosanbears.com",
     "삼성 라이온즈": "https://www.samsunglions.com",
     "KT 위즈": "https://www.ktwiz.co.kr",
     "한화 이글스": "https://www.hanwhaeagles.co.kr",
     "키움 히어로즈": "https://www.heroesbaseball.co.kr",
     "NC 다이노스": "https://www.ncdinos.com",
     "SSG 랜더스": "https://www.ssglanders.com"
}

#팀 연고지 정보
team_location={
    "KIA 타이거즈": "광주광역시",
    "롯데 자이언츠": "부산광역시",
    "LG 트윈스": "서울특별시",
    "두산 베어스": "서울특별시",
    "삼성 라이온즈": "대구광역시",
    "KT 위즈": "수원시",
    "한화 이글스": "대전광역시",
    "키움 히어로즈": "서울특별시",
    "NC 다이노스": "창원시",
    "SSG 랜더스": "인천광역시"
}

#팀당 우승횟수 
team_win={
    "KIA 타이거즈": "12회(1983, 1986~1989, 1991, 1993, 1996, 1997, 2009, 2017, 2024)",
    "롯데 자이언츠": "2회(1984, 1992)",
    "LG 트윈스": "3회(1990,1994,2023)",
    "두산 베어스": "6회(1982, 1995, 2001, 2015, 2016, 2019)",
    "삼성 라이온즈": "8회(1985, 2002, 2005, 2006, 2011~2014)",
    "KT 위즈": "1회(2021)",
    "한화 이글스": "1회(1999)",
    "키움 히어로즈": "-",
    "NC 다이노스": "1회(2020)",
    "SSG 랜더스": "5회(2007, 2008, 2010, 2018, 2022)"
}

#팀 색 가져오기
team_color={
    "KIA 타이거즈": "#EA0029",
    "롯데 자이언츠": "#041E42",
    "LG 트윈스": "#C30452",
    "두산 베어스": "#1A1748",
    "삼성 라이온즈": "#074CA1",
    "KT 위즈": "#000000",
    "한화 이글스": "#FC4E00",
    "키움 히어로즈": "#570514",
    "NC 다이노스": "#315288",
    "SSG 랜더스": "#CE0E2D"
}

team_code_id={
    "KIA 타이거즈": "HT",
    "롯데 자이언츠": "LT",
    "LG 트윈스": "LG",
    "두산 베어스": "OB",
    "삼성 라이온즈": "SS",
    "KT 위즈": "KT",
    "한화 이글스": "HH",
    "키움 히어로즈": "WO",
    "NC 다이노스": "NC",
    "SSG 랜더스": "SK"
}
# URL을 DB로 변경
team_name = {
    "KIA_TIGERS": "KIA 타이거즈",
    "LOTTE_GIANTS": "롯데 자이언츠",
    "LG_TWINS": "LG 트윈스",
    "DOOSAN_BEARS": "두산 베어스",
    "SAMSUNG_LIONS": "삼성 라이온즈",
    "KT_WIZ": "KT 위즈",
    "KIWOOM_HEROS": "키움 히어로즈",
    "NC_DIONS": "NC 다이노스",
    "SSG_LANDERS": "SSG 랜더스",
    "HANWHA_EAGLES" : "한화 이글스"
}
#DB를 URL로 변경
team_id = {
    "KIA 타이거즈" : "KIA_TIGERS",
    "롯데 자이언츠" : "LOTTE_GIANTS",
    "LG 트윈스" : "LG_TWINS",
    "두산 베어스" : "DOOSAN_BEARS",
    "삼성 라이온즈" : "SAMSUNG_LIONS",
    "KT 위즈" : "KT_WIZ",
    "키움 히어로즈" : "KIWOOM_HEROS",
    "NC 다이노스" : "NC_DIONS",
    "SSG 랜더스" : "SSG_LANDERS",
    "한화 이글스" : "HANWHA_EAGLES"
}

player_db = {
    "KIA_TIGERS": "kia_player",
    "LOTTE_GIANTS": "lotte_player",
    "LG_TWINS": "lg_player",
    "DOOSAN_BEARS": "dosan_player",
    "SAMSUNG_LIONS": "samsung_player",
    "KT_WIZ": "kt_player",
    "KIWOOM_HEROS": "kiwoom_player",
    "NC_DINOS": "nc_player",
    "SSG_LANDERS": "ssg_player",
    "HANWHA_EAGLES" : "hanwha_player"
}

headers={'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}

#팀 뉴스기사 가져오기 
def get_kbo_news(team_name):
    driver.get("https://www.koreabaseball.com/MediaNews/News/BreakingNews/List.aspx")
    time.sleep(1)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    items = soup.select("ul.boardPhoto > li")

    news_list = []
    for item in items:
        title_tag = item.select_one("strong > a")
        content_tag = item.select_one(".txt p")
        date_tag = item.select_one("span.date")
        image_tag = item.select_one(".boardPhoto .photo > a img")

        if title_tag:
            href = title_tag.get('href', '')
            if href.startswith("http"):
                link = href
            elif href.startswith("View.aspx"):
                link = "https://www.koreabaseball.com/MediaNews/News/BreakingNews/" + href
            elif href.startswith("/"):
                link = "https://www.koreabaseball.com" + href
            else:
                link = "https://www.koreabaseball.com/" + href

            news = {
                "title": title_tag.get_text(strip=True),
                "link": link,
                "content": content_tag.get_text(strip=True) if content_tag else "",
                "date": date_tag.get_text(strip=True) if date_tag else "",
                "image":image_tag['src'] if image_tag and image_tag.has_attr('src') else ""
            }

            # 팀이름필터링
            title = unicodedata.normalize('NFKC', news["title"])

            if team_name.split()[0] in title:
                news_list.append(news)
        if len(news_list)==5:
            break
    return news_list

# 스크랩 지옥 시작
def scrapStart(team_name): 
    #동적 반복
    query=f"{team_name}"
    uri=f"https://search.naver.com/search.naver?query={query}"
    res=requests.get(uri,headers=headers)
    soup=BeautifulSoup(res.text,'html.parser')

#팀 이미지 가져오기
    team_image=soup.select_one('.api_cs_wrap .thmb img')
    image_uri=team_image['src']if team_image and team_image.has_attr('src')else ""

#팀당 감독 들고오기
    team_manage=soup.select_one('.detail .class_etcinfo_sportsgame_managerTitle + dd a')
    manager=team_manage.get_text(strip=True) if team_manage else ""
            

#팀 별 경기일정 가져오기 
    team_id=team_code_id[team_name]
    uri=f"https://www.koreabaseball.com/Schedule/Schedule.aspx?seriesId=0&teamId={team_id}"
    driver.get(uri)
    time.sleep(1)

    soup=BeautifulSoup(driver.page_source, 'html.parser')
    rows=soup.select('table.tbl >tbody>tr')

    schedule_list=[]
    current_date=""

    for row in rows:
        tds = row.find_all("td")
    
    # 최소한 날짜, 시간, 팀1, vs, 팀2가 있어야 함
    
        if 'day' in tds[0].get("class", []):
            current_date = tds[0].get_text(strip=True)
            time_ = tds[1].get_text(strip=True)
            team1 = tds[2].get_text(strip=True)
            team2 = tds[4].get_text(strip=True)
        else:
            time_ = tds[0].get_text(strip=True)
            team1 = tds[1].get_text(strip=True)
            team2 = tds[3].get_text(strip=True)

        short_name=team_name.split()[0].replace(" ","")
        if short_name not in (team1+team2).replace(" ",""):
            continue

        game = {
            "date": current_date,
            "time": time_,
            "teams": f"{team1}{team2}"
            }
        
        schedule_list.append(game)

    #뉴스 기사 가져오기
    news_list=get_kbo_news(team_name)

    now=time.time()
    doc={
        "team_name":team_name,
        "team_image":image_uri,
        "team_location":team_location[team_name],
        "team_manage":manager,
        "team_win":team_win[team_name],
        "team_color":team_color[team_name],
        "team_homepage":team_homepage[team_name],
        "team_schedule": schedule_list,
        "team_news":news_list,
        "lastUpdatedTime": now
    }

    # teams_col.insert_one(doc)
    teams_col.replace_one({"team_name":team_name},doc,upsert=True)

def dbcall(teamName):
    target = teams_col.find_one({"team_name":teamName})
    doc={
        "team_name":teamName,
        "team_image":target['team_image'],
        "team_location":team_location[teamName],
        "team_manage":target['team_manage'],
        "team_win":team_win[teamName],
        "team_color":team_color[teamName],
        "team_homepage":team_homepage[teamName], 
        "team_schedule": target['team_schedule'],#리스트 객체인뎁숑
        "team_news":target['team_news'], #얘도 똑같애염
        "lastUpdatedTime": target['lastUpdatedTime']
    }


#DB에서 팀별 댓글 추출 API 응답하는 부분
@team_page.route('/<teamName>/playerId=<pId>/comment', methods=['GET'])
def get_team_comments(teamName,pId):

    # 댓글 DB중 해당하는 선수의 댓글 추출 후 리스트화
    comments = list(db.team_comment.find({'team_id': name}, {'_id': False}))
    return jsonify({'result': 'success', 'comments': comments})


# 댓글 등록 api 응답하는 부분
@team_page.route('/<teamName>/comment', methods =['POST'])
def post_comment(teamName):
 
     # 입력받은 Comment 데이터 가져오기
    input_comment = request.form.get('comment','').strip()

    if(input_comment == ''):
        return jsonify({'result': 'fail', 'msg': '내용을 입력하세요.'})

    #세션된 ID,닉네임 가져오기
    target_user = session.get('id')
    target_nickname = session.get('nickname')

    # 영어를 한글로
    name = team_name[teamName]
    # DB에 도큐멘트 형태로 변환
    doc = {
        'team_id': name, 'id' : target_user, 'nickname' :target_nickname, 'comment' : input_comment,  'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S') } #좋아요 추가시 user db와 이름혼동문제 
    db.team_comment.insert_one(doc)
    # DB에 아이디, 닉네임과 댓글 내용 데이터 저장
    # 댓글 등록 성공 (응답 성공 반환)
    return jsonify( {'result': 'success','msg' : '댓글 등록 성공!', 'nickname' : target_nickname, 'url' : f'{teamName}'})
    

#팀 페이지 라우팅 
@team_page.route('/<teamName>')
def team_detail(teamName):
    now = time.time()
    target=teams_col.find_one()
    lastUpdatedTime = float(target['lastUpdatedTime'])
    
    name = team_name[teamName] #SSG_LANDERS -> SSG 랜더스

    if now - lastUpdatedTime >=3600:
        scrapStart(name)
    else: 
        dbcall(name)

    # # lastUpdatedTime = db.teams_col.find_one({})

    #팀 정보 객체 찾아서 리디렉션과 동시에 던져줌
    team_data=teams_col.find_one({'team_name' : name}, {'_id' : 0})


    return render_template("teampage.html",team=team_data, nickname = session.get('nickname','익명'))


# def scrapOne(pId):
    
#     URL = f'https://www.koreabaseball.com/Record/Retire/Hitter.aspx?playerId={pId}';



#팀 / 선수 세부 페이지 라우팅
@team_page.route('/<teamName>/playerId=<pId>')
def player_detail(teamName, pId):

    #컬렉션 이름 가져오기
    collection_name = player_db.get(teamName)

    #컬렉션 접근
    collection = db[collection_name]
    # DB에서 데이터 불러오기
    target = collection.find_one({'playerId' : pId}, {'_id' : 0})

    # 시간 확인
    now = time.time()
    lastUpdatedTime = float(target['lastUpdatedTime'])

    #사흘마다 선수 데이터 동적으로 가져와서 저장
    if now - lastUpdatedTime >= 3600 * 24 * 3:
        #스크랩하는 함수
        player.scrapAllPlayer(target['name'])
    else:
        #해당 선수 정보 DB에서 가져오기
        pData = collection.find_one({'playerId' : pId}, {'_id' : 0})

    return render_template("player.html",player=pData, nickname = session.get('nickname','익명'))




#DB에서 선수별 댓글 추출 API 응답하는 부분
@team_page.route('/<teamname>/playerId=<pId>/comment', methods=['GET'])
def get_player_comments(teamName, pId):

    #컬렉션 이름 가져오기
    collection_name = player_db.values(pId)
    #컬렉션 접근
    collection = db[collection_name]
    player = collection.find_one({'playerId': pId}, {'_id': 0, 'player_comment_list': 1})
    comment_list = player.get('player_comment_list', []) if player else []

    return jsonify({'result': 'success', 'comments': comment_list})


# 선수 댓글 등록 api 응답하는 부분
@team_page.route('/<teamName>/playerId=<pId>/comment', methods =['POST'])
def post_player_comment(teamName,pId):
    print("응답 왔음")
     # 입력받은 Comment 데이터 가져오기
    input_comment = request.form.get('comment','').strip()
    
    if(input_comment == ''):
        return jsonify({'result': 'fail', 'msg': '내용을 입력하세요.'})


    #세션된 ID,닉네임 가져오기
    target_user = session.get('id')
    target_nickname = session.get('nickname')


    #컬렉션 이름 가져오기
    collection_name = player_db.get(teamName)

    

    #컬렉션 접근
    collection = db[collection_name]
    
    print(collection)

    # 해당 팀의 전체 선수 이름 추출 
    team_player_name =collection.find({}, {"name": 1})

     # 전체 선수중 타겟 선수 찾기
    for player in team_player_name:
        target_player_name = player.get("name")
        if not target_player_name:
            continue
    
    # DB의 각 팀별 컬렉션에서 해당 선수의 도큐멘트 형태로 변환
    collection.update_one(
           {"playerId": str(pId)},  # 정확한 타겟팅
        {"$push": {
            "player_comment_list": {
                "id": target_user,
                "nickname": target_nickname,
                "comment": input_comment,
                "date": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
        }}
    )
    # DB에 아이디, 닉네임과 댓글 내용 데이터 저장
    # 댓글 등록 성공 (응답 성공 반환)
    return jsonify( {'result': 'success','msg' : '댓글 등록 성공!', 'nickname' : target_nickname, 'url' : f'/team/{teamName}/playerId={pId}'})